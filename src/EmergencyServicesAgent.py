"""
Emergency Services Agent
Handles emergency service queries using SQL database
Based on Week 5A implementation
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


class EmergencyServicesAgent:
    """
    Emergency Services Agent for finding emergency facilities

    Features:
    - Query emergency services by zip code
    - Find hospitals with ambulance services
    - Get emergency contact information
    - Locate nearest emergency facilities
    """

    def __init__(
        self,
        emergency_csv_path: str = "data/hospitals_emergency_data.csv",
        db_path: str = "src/emergency.db",
        model_name: str = MODEL_NAME,
        api_key: str = OPENAI_API_KEY
    ):
        """
        Initialize Emergency Services Agent

        Args:
            emergency_csv_path: Path to emergency data CSV file
            db_path: Path to SQLite database
            model_name: OpenAI model name
            api_key: OpenAI API key
        """
        self.emergency_csv_path = emergency_csv_path
        self.db_path = db_path
        self.model_name = model_name
        self.api_key = api_key

        # Initialize database and agent
        self._setup_database()
        self._setup_agent()

    def _setup_database(self):
        """Setup SQLite database with emergency directory table"""
        try:
            # Create database connection
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Create emergency_directory table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS emergency_directory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                zip_code TEXT NOT NULL,
                hospital_name TEXT NOT NULL,
                ambulance_available TEXT NOT NULL
            )
            """)

            # Load and insert data if CSV exists
            if os.path.exists(self.emergency_csv_path):
                df = pd.read_csv(self.emergency_csv_path)
                df.to_sql("emergency_directory", conn, if_exists="replace", index=False)
                print(f"✅ Loaded {len(df)} emergency records into database")
            else:
                print(f"⚠️ Emergency CSV not found: {self.emergency_csv_path}")

            conn.commit()
            conn.close()

            print(f"✅ Emergency database setup complete: {self.db_path}")

        except Exception as e:
            print(f"❌ Error setting up database: {e}")
            raise

    def _setup_agent(self):
        """Setup LangChain SQL agent for querying emergency database"""
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
                    "\nUse LIKE operator when matching zip codes or hospital names.\n"
                    "Focus on finding nearest emergency services based on zip code.\n"
                    "Prioritize hospitals with ambulance availability.\n"
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

            print("✅ Emergency Services Agent initialized successfully")

        except Exception as e:
            print(f"❌ Error setting up agent: {e}")
            raise

    def query(self, user_input: str) -> Dict[str, Any]:
        """
        Process user query about emergency services

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

    def find_emergency_services(self, zip_code: str) -> Dict[str, Any]:
        """
        Find emergency services in a specific zip code

        Args:
            zip_code: Zip code to search

        Returns:
            Dict with emergency services information
        """
        try:
            query = f"Find all emergency services in zip code {zip_code}"
            return self.query(query)

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": None
            }

    def find_ambulance_services(self, zip_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Find hospitals with ambulance services

        Args:
            zip_code: Optional zip code filter

        Returns:
            Dict with ambulance services information
        """
        try:
            if zip_code:
                query = f"Show me all hospitals with ambulance services in zip code {zip_code}"
            else:
                query = "Show me all hospitals with ambulance services"

            return self.query(query)

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": None
            }

    def get_nearest_emergency(self, zip_code: str) -> Dict[str, Any]:
        """
        Get nearest emergency facility

        Args:
            zip_code: User's zip code

        Returns:
            Dict with nearest emergency facility info
        """
        try:
            query = f"What is the nearest emergency facility to zip code {zip_code}?"
            return self.query(query)

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": None
            }

    def check_ambulance_availability(self, hospital_name: str) -> Dict[str, Any]:
        """
        Check if a specific hospital has ambulance service

        Args:
            hospital_name: Name of the hospital

        Returns:
            Dict with ambulance availability info
        """
        try:
            query = f"Does {hospital_name} have ambulance service available?"
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
    print("TESTING EMERGENCY SERVICES AGENT")
    print("="*80)

    try:
        # Initialize agent
        agent = EmergencyServicesAgent()

        # Test queries
        test_queries = [
            "Find emergency services in zip code 10001",
            "Show me all hospitals with ambulance services",
            "What emergency facilities are available in 90210?",
            "Find nearest emergency room to 60601"
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
