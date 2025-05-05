from crewai import Task
from agents.idea_refinement_specialist import IdeaRefinementSpecialist
import logging

logger = logging.getLogger(__name__)


class IdeaRefinementTask:
    """Task for refining the generated seed ideas."""

    @staticmethod
    def create(seed_ideas=None):
        """
        Create a task for refining research ideas.

        Args:
            seed_ideas: The output from the idea generation task

        Returns:
            Task: A configured CrewAI task
        """
        logger.info("Creating idea refinement task")

        # Create the agent for this task
        agent = IdeaRefinementSpecialist.create()

        # Create task description with specific instructions
        task_description = (
            "Refine and enhance the generated seed ideas through critical analysis and strategic thinking. "
            "Evaluate each idea for scientific merit, feasibility, and potential impact. "
            "Identify weaknesses or challenges in the initial ideas and propose specific improvements. "
            "Consider practical aspects of implementation including methodology, required resources, and timeline. "
            "Enhance the scope or application potential where appropriate. "
            "Narrow overly broad concepts to more focused, executable research directions. "
            "Strike a balance between ambition and practicality in your refinements."
        )

        # Define expected output format with schema example
        expected_output = (
            "A JSON list of refined ideas with this structure:\n"
            "[\n"
            "  {\n"
            "    \"refined_idea_title\": \"Refined Title of Research Idea\",\n"
            "    \"original_idea_title\": \"Original Title from Seed Idea\",\n"
            "    \"description\": \"Enhanced description with improvements\",\n"
            "    \"methodology_outline\": \"Brief outline of proposed methodology\",\n"
            "    \"required_resources\": \"Description of necessary resources\",\n"
            "    \"estimated_timeline\": \"Estimated timeline for completion\",\n"
            "    \"potential_challenges\": [\"Challenge 1\", \"Challenge 2\"],\n"
            "    \"expected_impact\": \"Description of the expected impact\",\n"
            "    \"feasibility_score\": 7.5  // Rate from 1-10 how feasible this idea is\n"
            "  },\n"
            "  ...\n"
            "]\n"
        )

        return Task(
            description=task_description,
            expected_output=expected_output,
            agent=agent,
            context=[seed_ideas] if seed_ideas else [],
            async_execution=False
        )