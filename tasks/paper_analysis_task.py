from crewai import Task
from agents.research_paper_analyst import ResearchPaperAnalyst


class PaperAnalysisTask:
    """Task for analyzing the related papers to identify key knowledge and limitations."""

    @staticmethod
    def create(research_papers=None):
        """
        Create a task for analyzing research papers.

        Args:
            research_papers: The output from the paper finding task

        Returns:
            Task: A configured CrewAI task
        """
        agent = ResearchPaperAnalyst.create()

        return Task(
            description="Analyze the related papers to identify key knowledge and limitations.",
            expected_output="A JSON object summarizing key knowledge and limitations from the related papers.",
            agent=agent,
            context=[research_papers] if research_papers else [],
            async_execution=False
        )