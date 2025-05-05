from agents.base_agent import BaseAgent
from langchain_community.tools.tavily_search import TavilySearchResults


class ResearchPaperFinder:
    """Agent responsible for finding relevant research papers on a topic."""

    @staticmethod
    def create():
        search_tool = TavilySearchResults(max_results=5)

        return BaseAgent.create(
            name="Research Paper Finder",
            role="Research Paper Finder",
            goal="Find relevant scientific papers related to the input paper",
            backstory="You are an expert at finding relevant scientific papers "
                      "related to a given research topic.",
            tools=[search_tool]
        )