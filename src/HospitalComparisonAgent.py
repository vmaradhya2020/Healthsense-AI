"""
Hospital Comparison Agent
Compares hospitals based on various parameters like location, specialties, ratings, etc.
"""

from langchain_openai import ChatOpenAI
import pandas as pd
import os

# Custom Tool class (replaces CrewAI BaseTool to avoid Pydantic issues)
class PandasTool:
    """Custom tool for querying and analyzing hospital data using pandas"""
    def __init__(self):
        self.name = "pandas_tool"
        self.description = "Query and analyze hospital data using pandas"

    def run(self, query: str) -> str:
        """Execute a pandas query on hospital data"""
        try:
            df = pd.read_csv("data/Hospital_General_Information.csv")
            return f"Running query: {query}\nDataset shape: {df.shape}"
        except Exception as e:
            return f"Error running query: {str(e)}"

# Custom Agent class (lightweight alternative to CrewAI Agent)
class Agent:
    """Custom Agent class to replace CrewAI Agent"""
    def __init__(self, role, goal, backstory, tools=None, verbose=False):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools or []
        self.verbose = verbose

    def run(self, query: str) -> str:
        """Run the agent with the given query"""
        if self.verbose:
            print(f"[{self.role}] Processing: {query}")

        # Use first tool if available
        if self.tools:
            return self.tools[0].run(query)
        return f"Agent {self.role} processed: {query}"

class HospitalComparisonAgent:
    """
    Hospital Comparison Agent for analyzing and comparing hospitals
    """
    def __init__(self):
        self.hospital_info_agent = Agent(
            role='Hospital Information Analyst',
            goal='Compare hospitals based on various parameters',
            backstory='Expert in evaluating hospital data, patient reviews, and healthcare metrics',
            tools=[PandasTool()],
            verbose=True
        )

    def compare_hospitals(self, query: str) -> str:
        """
        Compare hospitals based on user query

        Args:
            query (str): User's comparison query

        Returns:
            str: Comparison results
        """
        return self.hospital_info_agent.run(query)
