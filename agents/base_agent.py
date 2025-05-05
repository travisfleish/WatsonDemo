from crewai import Agent
from models.watsonx_llm import llm


class BaseAgent:
    """Base agent class with common functionality for all agents."""

    @staticmethod
    def create(name, role, goal, backstory, tools=None):
        """
        Factory method to create a CrewAI agent with consistent configuration.

        Args:
            name (str): The agent's name
            role (str): The agent's role
            goal (str): The agent's goal
            backstory (str): The agent's backstory
            tools (list, optional): List of tools available to the agent

        Returns:
            Agent: A configured CrewAI agent
        """
        return Agent(
            name=name,
            role=role,
            goal=goal,
            backstory=backstory,
            verbose=True,
            llm=llm,
            tools=tools or []
        )