"""
Diagnostic Info Agent
Handles lab test and diagnostic information queries using Pandas DataFrame
Based on Week 5B implementation
"""

import os
import pandas as pd
import httpx
from typing import Optional, Dict, Any

from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain_core.prompts import SystemMessagePromptTemplate, ChatPromptTemplate

from src.constants import MODEL_NAME, OPENAI_API_KEY


class DiagnosticInfoAgent:
    """
    Diagnostic Information Agent for lab tests and health screening packages

    Features:
    - Query available lab tests
    - Get test pricing information
    - Find diagnostic packages
    - Compare lab tests across hospitals
    - Get recommendations for health screenings
    """

    def __init__(
        self,
        diagnostic_csv_path: str = "data/Hospital_Information_with_Lab_Tests.csv",
        model_name: str = MODEL_NAME,
        api_key: str = OPENAI_API_KEY
    ):
        """
        Initialize Diagnostic Info Agent

        Args:
            diagnostic_csv_path: Path to diagnostic/lab test CSV file
            model_name: OpenAI model name
            api_key: OpenAI API key
        """
        self.diagnostic_csv_path = diagnostic_csv_path
        self.model_name = model_name
        self.api_key = api_key

        # Load data and setup agent
        self._load_data()
        self._setup_agent()

    def _load_data(self):
        """Load diagnostic data from CSV"""
        try:
            if os.path.exists(self.diagnostic_csv_path):
                self.df = pd.read_csv(self.diagnostic_csv_path)
                print(f"✅ Loaded {len(self.df)} diagnostic records")
                print(f"📊 Columns: {', '.join(self.df.columns.tolist())}")
            else:
                raise FileNotFoundError(f"Diagnostic CSV not found: {self.diagnostic_csv_path}")

        except Exception as e:
            print(f"❌ Error loading data: {e}")
            raise

    def _setup_agent(self):
        """Setup LangChain Pandas DataFrame agent"""
        try:
            # Initialize OpenAI LLM with HTTP client that skips SSL verification
            # Note: In production, you should use proper SSL certificates
            self.llm = ChatOpenAI(
                openai_api_key=self.api_key,
                temperature=0,
                model=self.model_name,
                max_tokens=500,
                http_client=httpx.Client(verify=False)
            )

            # Create system message with detailed instructions
            system_message = SystemMessagePromptTemplate.from_template(
            """
            You are a highly skilled healthcare assistant with expertise in suggesting health screening tests and packages.
            Your task is to assess various hospitals based on a user's specific conditions, preferences, and needs.
            You will evaluate hospitals considering factors such as medical specialties, patient reviews, location, cost, accessibility, facilities,
            and the availability of treatment for specific conditions.

            When comparing hospitals or providing lab test information, follow these guidelines:

            - Condition-Specific Comparison: Focus on the hospitals' expertise in treating the user's specific health condition
            (e.g., heart disease, cancer, etc.).
            - Hospital Features: Include details about the hospital's reputation, technology, facilities, specialized care, and any awards or
            recognitions.
            - Location and Accessibility: Consider the proximity to the user's location and the convenience of travel.
            - Cost and Insurance: Compare the cost of treatment and insurance coverage options offered by the hospitals.
            - Patient Feedback: Analyze reviews and ratings to gauge patient satisfaction and outcomes.
            - Personalized Recommendation: Provide a clear, personalized suggestion based on the user's priorities, whether they are medical
            expertise, convenience, or cost.
            - Lab Test Information: When asked about lab tests, provide accurate information about test names, prices, availability, and
            which hospitals offer them.

            CAREFULLY look at each column name to understand what to output.
            Always provide concise, accurate, and helpful information.
            """
            )

            # Create prompt template
            prompt = ChatPromptTemplate.from_messages([system_message])

            # Create Pandas DataFrame agent
            self.agent = create_pandas_dataframe_agent(
                self.llm,
                self.df,
                prompt=prompt,
                verbose=False,
                allow_dangerous_code=True,
                agent_type=AgentType.OPENAI_FUNCTIONS
            )

            print("✅ Diagnostic Info Agent initialized successfully")

        except Exception as e:
            print(f"❌ Error setting up agent: {e}")
            raise

    def query(self, user_input: str) -> Dict[str, Any]:
        """
        Process user query about diagnostic tests and lab information

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
            result = self.agent.invoke(user_input)

            # Extract output (different structure than SQL agent)
            output = result.get("output", str(result)) if isinstance(result, dict) else str(result)

            return {
                "success": True,
                "output": output,
                "input": user_input
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": None,
                "input": user_input
            }

    def get_lab_test_info(self, test_name: str) -> Dict[str, Any]:
        """
        Get information about a specific lab test

        Args:
            test_name: Name of the lab test

        Returns:
            Dict with test information
        """
        try:
            query = f"Tell me about the {test_name} test. What hospitals offer it and what's the price?"
            return self.query(query)

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": None
            }

    def find_tests_by_condition(self, condition: str) -> Dict[str, Any]:
        """
        Find recommended tests for a specific health condition

        Args:
            condition: Health condition (e.g., "diabetes", "heart disease")

        Returns:
            Dict with recommended tests
        """
        try:
            query = f"What lab tests are recommended for {condition}?"
            return self.query(query)

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": None
            }

    def compare_test_prices(self, test_name: str) -> Dict[str, Any]:
        """
        Compare prices for a specific test across hospitals

        Args:
            test_name: Name of the test

        Returns:
            Dict with price comparison
        """
        try:
            query = f"Compare the prices for {test_name} across different hospitals. Show me the cheapest options."
            return self.query(query)

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": None
            }

    def get_health_screening_packages(self) -> Dict[str, Any]:
        """
        Get available health screening packages

        Returns:
            Dict with package information
        """
        try:
            query = "What health screening packages are available? List the comprehensive ones."
            return self.query(query)

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": None
            }

    def find_affordable_tests(self, max_price: Optional[float] = None) -> Dict[str, Any]:
        """
        Find affordable lab tests

        Args:
            max_price: Optional maximum price filter

        Returns:
            Dict with affordable tests
        """
        try:
            if max_price:
                query = f"Show me all lab tests that cost less than ${max_price}"
            else:
                query = "Show me the most affordable lab tests available"

            return self.query(query)

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": None
            }

    def get_dataset_info(self) -> Dict[str, Any]:
        """
        Get information about the dataset

        Returns:
            Dict with dataset statistics
        """
        try:
            return {
                "success": True,
                "rows": len(self.df),
                "columns": self.df.columns.tolist(),
                "sample": self.df.head(3).to_dict('records')
            }

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
    print("TESTING DIAGNOSTIC INFO AGENT")
    print("="*80)

    try:
        # Initialize agent
        agent = DiagnosticInfoAgent()

        # Get dataset info
        print("\n📊 Dataset Information:")
        print("-" * 80)
        info = agent.get_dataset_info()
        if info["success"]:
            print(f"Rows: {info['rows']}")
            print(f"Columns: {', '.join(info['columns'])}")

        # Test queries
        test_queries = [
            "What lab tests are available for diabetes screening?",
            "Show me the cheapest blood test options",
            "What health screening packages do you have?",
            "Tell me about Complete Blood Count (CBC) test"
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
