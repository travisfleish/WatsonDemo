from agents.base_agent import BaseAgent
from tools.tavily_search import TavilySearchTool
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
        # Create the search tool with academic domain focus
        search_tool = TavilySearchTool(
            max_results=7,
            search_depth="advanced",
            include_domains=[
                "scholar.google.com",
                "arxiv.org",
                "researchgate.net",
                "sciencedirect.com",
                "nature.com",
                "science.org",
                "pubmed.ncbi.nlm.nih.gov",
                "ieee.org",
                "acm.org",
                "jstor.org"
            ]
        )

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
            tools=[search_tool],
            system_prompt=system_prompt,
            verbose=True
        )