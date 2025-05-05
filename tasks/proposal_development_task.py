from crewai import Task
from agents.research_proposal_developer import ResearchProposalDeveloper


class ProposalDevelopmentTask:
    """Task for developing complete research proposals from refined ideas."""

    @staticmethod
    def create(refined_ideas=None):
        """
        Create a task for developing research proposals.

        Args:
            refined_ideas: The output from the idea refinement task

        Returns:
            Task: A configured CrewAI task
        """
        agent = ResearchProposalDeveloper.create()

        return Task(
            description="Develop a complete research proposal based on the refined research ideas.",
            expected_output="A JSON list of research proposals including proposal_title, methodology, and expected_outcomes.",
            agent=agent,
            context=[refined_ideas] if refined_ideas else [],
            async_execution=False
        )