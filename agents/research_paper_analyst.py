from agents.base_agent import BaseAgent
from tools.scrape_website import scrape_website  # Import the function instead of the class
from utils.helpers import load_prompt_template


class ResearchPaperAnalyst(BaseAgent):
    """Agent responsible for analyzing research papers and extracting key insights."""

    @staticmethod
    def create():
        """
        Factory method to create a Research Paper Analyst agent.

        Returns:
            Agent: A configured CrewAI agent for analyzing research papers
        """
        # Load the system prompt from templates
        system_prompt = load_prompt_template("research_paper_analyst")

        return BaseAgent.create(
            name="Research Paper Analyst",
            role="Research Paper Analyst",
            goal="Analyze scientific papers to extract key knowledge and limitations",
            backstory="You are an expert at analyzing scientific papers to identify "
                      "key findings, methodologies, and limitations. You excel at "
                      "synthesizing information across multiple papers to identify "
                      "patterns, contradictions, and research gaps.",
            tools=[scrape_website],  # Pass the function directly
            system_prompt=system_prompt,
            verbose=True
        )