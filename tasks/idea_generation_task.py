from crewai import Task
from agents.seed_idea_generator import SeedIdeaGenerator
import logging

logger = logging.getLogger(__name__)


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
        logger.info("Creating idea generation task")

        # Create the agent for this task
        agent = SeedIdeaGenerator.create()

        # Create task description with specific instructions
        task_description = (
            "Generate 3-5 novel research ideas based on the knowledge and limitations identified in the analyzed papers. "
            "Identify gaps and opportunities in the existing research landscape. "
            "Generate creative connections between different concepts and findings. "
            "Propose ideas that build upon the strengths of existing research while addressing identified limitations. "
            "Consider interdisciplinary angles that might yield fresh insights. "
            "Each idea should be ambitious yet feasible with current technology and methods. "
            "Focus on originality and potential impact rather than incremental improvements."
        )

        # Define expected output format with schema example
        expected_output = (
            "A JSON list of research ideas with this structure:\n"
            "[\n"
            "  {\n"
            "    \"idea_title\": \"Title of Research Idea\",\n"
            "    \"description\": \"Detailed description of the research idea\",\n"
            "    \"rationale\": \"Explanation of why this idea is valuable and how it addresses gaps\",\n"
            "    \"related_papers\": [\"Paper Title 1\", \"Paper Title 2\"],\n"
            "    \"novelty_score\": 8.5  // Rate from 1-10 how novel this idea is\n"
            "  },\n"
            "  ...\n"
            "]\n"
        )

        return Task(
            description=task_description,
            expected_output=expected_output,
            agent=agent,
            context=[research_papers_analysis] if research_papers_analysis else [],
            async_execution=False
        )