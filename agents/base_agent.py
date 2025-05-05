from crewai import Agent
from models.watsonx_llm import llm
import logging

logger = logging.getLogger(__name__)


class BaseAgent:
    """Base agent class with common functionality for all agents."""

    @staticmethod
    def create(name, role, goal, backstory, tools=None, system_prompt=None, verbose=True):
        """
        Factory method to create a CrewAI agent with consistent configuration.

        Args:
            name (str): The agent's name
            role (str): The agent's role
            goal (str): The agent's goal
            backstory (str): The agent's backstory
            tools (list, optional): List of tools available to the agent
            system_prompt (str, optional): Custom system prompt for the agent
            verbose (bool, optional): Whether to enable verbose logging

        Returns:
            Agent: A configured CrewAI agent
        """
        try:
            logger.info(f"Creating agent: {name}")

            # Create the agent with the provided parameters
            agent = Agent(
                name=name,
                role=role,
                goal=goal,
                backstory=backstory,
                verbose=verbose,
                llm=llm,
                tools=tools or [],
                system_prompt=system_prompt
            )

            logger.info(f"Successfully created agent: {name}")
            return agent

        except Exception as e:
            logger.error(f"Error creating agent {name}: {str(e)}")
            raise