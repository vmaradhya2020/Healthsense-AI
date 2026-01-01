"""
Doctor Information Agent
Handles doctor appointment queries and booking using SQL database
Based on Week 4 implementation
"""

import os
import sqlite3
import pandas as pd
from typing import Optional, Dict, Any

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.prompt import SQL_FUNCTIONS_SUFFIX
from langchain_community.utilities import SQLDatabase
from langchain_core.messages import AIMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_openai import ChatOpenAI

from src.constants import MODEL_NAME, OPENAI_API_KEY


class DoctorInfoAgent:
    """
    Doctor Information Agent for handling doctor appointments

    Features:
    - Query available doctors by specialization
    - Check available appointment slots
    - Book appointments
    - Get doctor information
    """

    def __init__(
        self,
        doctors_csv_path: str = "data/doctors_info_data.csv",
        slots_csv_path: str = "data/doctors_slots_data.csv",
        db_path: str = "src/appointments.db",
        model_name: str = MODEL_NAME,
        api_key: str = OPENAI_API_KEY
    ):
        """
        Initialize Doctor Info Agent

        Args:
            doctors_csv_path: Path to doctors CSV file
            slots_csv_path: Path to slots CSV file
            db_path: Path to SQLite database
            model_name: OpenAI model name
            api_key: OpenAI API key
        """
        self.doctors_csv_path = doctors_csv_path
        self.slots_csv_path = slots_csv_path
        self.db_path = db_path
        self.model_name = model_name
        self.api_key = api_key

        # Initialize database and agent
        self._setup_database()
        self._setup_agent()

    def _setup_database(self):
        """Setup SQLite database with doctors and slots tables"""
        try:
            # Create database connection
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Create doctors table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER,
                name TEXT NOT NULL,
                specialization TEXT NOT NULL,
                contact TEXT NOT NULL
            )
            """)

            # Create slots table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS slots (
                id INTEGER,
                doctor_id INTEGER NOT NULL,
                datetime TEXT NOT NULL,
                is_available BOOLEAN NOT NULL
            )
            """)

            # Load and insert data if CSV files exist
            if os.path.exists(self.doctors_csv_path):
                df_doctors = pd.read_csv(self.doctors_csv_path)
                df_doctors.to_sql("doctors", conn, if_exists="replace", index=False)
                print(f"✅ Loaded {len(df_doctors)} doctors into database")
            else:
                print(f"⚠️ Doctors CSV not found: {self.doctors_csv_path}")

            if os.path.exists(self.slots_csv_path):
                df_slots = pd.read_csv(self.slots_csv_path)
                df_slots.to_sql("slots", conn, if_exists="replace", index=False)
                print(f"✅ Loaded {len(df_slots)} appointment slots into database")
            else:
                print(f"⚠️ Slots CSV not found: {self.slots_csv_path}")

            conn.commit()
            conn.close()

            print(f"✅ Database setup complete: {self.db_path}")

        except Exception as e:
            print(f"❌ Error setting up database: {e}")
            raise

    def _setup_agent(self):
        """Setup LangChain SQL agent for querying database"""
        try:
            # Initialize OpenAI LLM
            self.llm = ChatOpenAI(
                model=self.model_name,
                temperature=0,
                openai_api_key=self.api_key
            )

            # Connect to database via LangChain
            self.db = SQLDatabase.from_uri(f"sqlite:///{self.db_path}")

            # Create SQL Toolkit
            self.toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)

            # Get context and tools
            context = self.toolkit.get_context()
            tools = self.toolkit.get_tools()

            # Define prompt messages
            messages = [
                HumanMessagePromptTemplate.from_template("{input}"),
                AIMessage(
                    content=SQL_FUNCTIONS_SUFFIX +
                    "\nUse LIKE operator with lowercase when matching a name.\n"
                    "When a user requests to book slots, delete the corresponding row from the table.\n"
                ),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ]

            # Create prompt template
            prompt = ChatPromptTemplate.from_messages(messages)
            prompt = prompt.partial(**context)

            # Create agent
            agent = create_openai_tools_agent(self.llm, tools, prompt)

            # Create agent executor
            self.agent_executor = AgentExecutor(
                agent=agent,
                tools=tools,
                verbose=True
            )

            print("✅ Doctor Info Agent initialized successfully")

        except Exception as e:
            print(f"❌ Error setting up agent: {e}")
            raise

    def query(self, user_input: str) -> Dict[str, Any]:
        """
        Process user query about doctors or appointments

        Args:
            user_input: User's natural language query

        Returns:
            Dict containing response and metadata
        """
        try:
            if not user_input or not user_input.strip():
                return {
                    "success": False,
                    "error": "Query cannot be empty",
                    "output": None
                }

            # Invoke agent
            result = self.agent_executor.invoke({"input": user_input})

            return {
                "success": True,
                "output": result.get("output", "No response generated"),
                "input": user_input
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": None,
                "input": user_input
            }

    def get_available_doctors(self, specialization: Optional[str] = None) -> Dict[str, Any]:
        """
        Get list of available doctors

        Args:
            specialization: Optional filter by specialization

        Returns:
            Dict with doctors list
        """
        try:
            if specialization:
                query = f"Show me all doctors specialized in {specialization}"
            else:
                query = "Show me all available doctors"

            return self.query(query)

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": None
            }

    def get_available_slots(self, doctor_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get available appointment slots

        Args:
            doctor_name: Optional filter by doctor name

        Returns:
            Dict with available slots
        """
        try:
            if doctor_name:
                query = f"Show me available appointment slots for Dr. {doctor_name}"
            else:
                query = "Show me all available appointment slots"

            return self.query(query)

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": None
            }

    def book_appointment(self, doctor_name: str, slot_time: str) -> Dict[str, Any]:
        """
        Book an appointment slot

        Args:
            doctor_name: Doctor's name
            slot_time: Appointment time (e.g., "3PM", "10:00 AM")

        Returns:
            Dict with booking confirmation
        """
        try:
            query = f"Book {slot_time} slot for Dr. {doctor_name}"
            return self.query(query)

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": None
            }

    def get_doctor_info(self, doctor_name: str) -> Dict[str, Any]:
        """
        Get information about a specific doctor

        Args:
            doctor_name: Doctor's name

        Returns:
            Dict with doctor information
        """
        try:
            query = f"Tell me about Dr. {doctor_name}"
            return self.query(query)

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": None
            }


# Example usage and testing
if __name__ == "__main__":
    # Test the agent
    print("\n" + "="*80)
    print("TESTING DOCTOR INFO AGENT")
    print("="*80)

    try:
        # Initialize agent
        agent = DoctorInfoAgent()

        # Test queries
        test_queries = [
            "Show me all cardiologists",
            "What slots are available for Dr. Elizabeth Moore?",
            "Book 3PM slot for Dr. Elizabeth Moore",
            "Show me all available doctors"
        ]

        for query in test_queries:
            print(f"\n📝 Query: {query}")
            print("-" * 80)
            result = agent.query(query)
            if result["success"]:
                print(f"✅ Response: {result['output']}")
            else:
                print(f"❌ Error: {result['error']}")

        print("\n" + "="*80)
        print("TESTING COMPLETE")
        print("="*80)

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
