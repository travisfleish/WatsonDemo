from agents.base_agent import BaseAgent
from crewai_tools import ScrapeWebsiteTool


class ResearchPaperAnalyst:
    """Agent responsible for analyzing research papers and extracting key insights."""

    @staticmethod
    def create():
        scrape_tool = ScrapeWebsiteTool()

        return BaseAgent.create(
            name="Research Paper Analyst",
            role="Research Paper Analyst",
            goal="Analyze scientific papers to extract key knowledge and limitations",
            backstory="You are an expert at analyzing scientific papers to identify "
                      "key findings, methodologies, and limitations.",
            tools=[scrape_tool]
        )