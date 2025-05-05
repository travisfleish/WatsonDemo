from crewai import Task
from agents.seed_idea_generator import SeedIdeaGenerator


class IdeaGenerationTask:
    """Task for generating initial research ideas based on paper analysis."""

    @staticmethod
    def create(research_papers_analysis=None):
        """
        Create a task for generating initial research ideas.

        Args:
            research_papers_analysis: The output from the paper analysis task

        Returns:
            Task: A configured CrewAI task
        """
        agent = SeedIdeaGenerator.create()

        return Task(
            description="Generate initial research ideas based on the knowledge and limitations provided in the analyzed papers.",
            expected_output="A JSON list of research ideas including idea_title, description, and rationale.",
            agent=agent,
            context=[research_papers_analysis] if research_papers_analysis else [],
            async_execution=False
        )