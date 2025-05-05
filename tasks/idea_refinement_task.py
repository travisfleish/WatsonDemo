from crewai import Task
from agents.idea_refinement_specialist import IdeaRefinementSpecialist


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
        agent = IdeaRefinementSpecialist.create()

        return Task(
            description="Refine the generated seed ideas by expanding and identifying key improvements.",
            expected_output="A JSON list of refined ideas including refined_idea_title, description, and impact.",
            agent=agent,
            context=[seed_ideas] if seed_ideas else [],
            async_execution=False
        )