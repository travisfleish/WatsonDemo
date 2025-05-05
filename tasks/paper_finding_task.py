from crewai import Task
from agents.research_paper_finder import ResearchPaperFinder


class PaperFindingTask:
    """Task for finding relevant scientific papers."""

    @staticmethod
    def create(input_paper):
        """
        Create a task for finding relevant scientific papers.

        Args:
            input_paper: The title of the input paper to search for related papers

        Returns:
            Task: A configured CrewAI task
        """
        agent = ResearchPaperFinder.create()

        return Task(
            description=f"Find related scientific papers for '{input_paper}' using web search.",
            expected_output="A JSON list of papers including title, authors, url and summary.",
            agent=agent,
            context=[],
            async_execution=False
        )