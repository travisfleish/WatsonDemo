from crewai import Task
from agents.research_proposal_developer import ResearchProposalDeveloper
import logging
import json

logger = logging.getLogger(__name__)


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
        logger.info("Creating proposal development task")

        # Create the agent for this task
        agent = ResearchProposalDeveloper.create()

        # Convert refined_ideas to a string for the task description
        ideas_str = ""
        if refined_ideas is not None:
            if isinstance(refined_ideas, (list, dict)):
                ideas_str = json.dumps(refined_ideas, indent=2)
            else:
                ideas_str = str(refined_ideas)

        # Create task description with specific instructions
        task_description = (
            "Transform the refined research ideas into complete, well-structured research proposals. "
            "For each idea, develop a formal research proposal with clear objectives, hypotheses, and significance. "
            "Include detailed methodology sections that outline specific approaches, techniques, and experimental designs. "
            "Define expected outcomes and their significance to the field. "
            "Address potential challenges and provide mitigation strategies. "
            "Consider ethical implications and necessary approvals where relevant. "
            "Outline resource requirements and approximate timelines for different phases. "
            "Write in a formal, academic style appropriate for research proposals.\n\n"
            f"Here are the refined ideas to develop into proposals:\n{ideas_str}"
        )

        # Define expected output format with schema example - USE TRIPLE QUOTES AND ESCAPE BRACES
        expected_output = """A JSON list of research proposals with this structure:
[
  {{
    "proposal_title": "Final Research Proposal Title",
    "refined_idea_title": "Title from Refined Idea",
    "introduction": "Introduction and background of the research problem",
    "research_questions": ["Question 1", "Question 2"],
    "hypotheses": ["Hypothesis 1", "Hypothesis 2"],
    "methodology": "Detailed description of methodology and approaches",
    "expected_outcomes": "Description of expected outcomes and significance",
    "potential_challenges": "Challenges and mitigation strategies",
    "ethical_considerations": "Relevant ethical considerations",
    "resource_requirements": "Required resources and budget considerations",
    "timeline": "Projected timeline for research phases",
    "references": ["Reference 1", "Reference 2"]
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