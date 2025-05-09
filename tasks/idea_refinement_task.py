from crewai import Task
from agents.idea_refinement_specialist import IdeaRefinementSpecialist
import logging
import json

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

        # Convert seed_ideas to a string for the task description
        ideas_str = ""
        if seed_ideas is not None:
            if isinstance(seed_ideas, (list, dict)):
                ideas_str = json.dumps(seed_ideas, indent=2)
            else:
                ideas_str = str(seed_ideas)

        # Create task description with specific instructions
        task_description = (
            "Refine and enhance the generated seed ideas through critical analysis and strategic thinking. "
            "Evaluate each idea for scientific merit, feasibility, and potential impact. "
            "Identify weaknesses or challenges in the initial ideas and propose specific improvements. "
            "Consider practical aspects of implementation including methodology, required resources, and timeline. "
            "Enhance the scope or application potential where appropriate. "
            "Narrow overly broad concepts to more focused, executable research directions. "
            "Strike a balance between ambition and practicality in your refinements.\n\n"
            f"Here are the seed ideas to refine:\n{ideas_str}"
        )

        # Define expected output format with schema example - USE TRIPLE QUOTES AND ESCAPE BRACES
        expected_output = """A JSON list of refined ideas with this structure:
[
  {{
    "refined_idea_title": "Refined Title of Research Idea",
    "original_idea_title": "Original Title from Seed Idea",
    "description": "Enhanced description with improvements",
    "methodology_outline": "Brief outline of proposed methodology",
    "required_resources": "Description of necessary resources",
    "estimated_timeline": "Estimated timeline for completion",
    "potential_challenges": ["Challenge 1", "Challenge 2"],
    "expected_impact": "Description of the expected impact",
    "feasibility_score": 7.5  // Rate from 1-10 how feasible this idea is
  }},
  ...
]
"""

        return Task(
            description=task_description,
            expected_output=expected_output,
            agent=agent,
            context=[],  # Use empty list like paper_finding_task
            async_execution=False
        )