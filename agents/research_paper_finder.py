from agents.base_agent import BaseAgent
from tools.tavily_search import tavily_search  # Import the function instead of the class
from utils.helpers import load_prompt_template


class ResearchPaperFinder(BaseAgent):
    """Agent responsible for finding relevant research papers on a topic."""

    @staticmethod
    def create():
        """
        Factory method to create a Research Paper Finder agent.

        Returns:
            Agent: A configured CrewAI agent for finding research papers
        """
        # Load the system prompt from templates
        system_prompt = load_prompt_template("research_paper_finder")

        return BaseAgent.create(
            name="Research Paper Finder",
            role="Research Paper Finder",
            goal="Find relevant scientific papers related to the input paper",
            backstory="You are an expert at finding relevant scientific papers "
                      "related to a given research topic. You focus on recent, "
                      "high-quality papers from reputable sources and deliver "
                      "comprehensive results with accurate metadata.",
            tools=[tavily_search],  # Pass the function directly
            system_prompt=system_prompt,
            verbose=True
        )