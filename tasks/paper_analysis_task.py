from crewai import Task
from agents.research_paper_analyst import ResearchPaperAnalyst
import logging
import json

logger = logging.getLogger(__name__)


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
        logger.info("Creating paper analysis task")

        # Create the agent for this task
        agent = ResearchPaperAnalyst.create()

        # Convert research_papers to a string for the task description
        papers_str = ""
        if research_papers is not None:
            if isinstance(research_papers, (list, dict)):
                papers_str = json.dumps(research_papers, indent=2)
            else:
                papers_str = str(research_papers)

        # Create task description with specific instructions
        task_description = (
            "Analyze the related papers to identify key knowledge, methodologies, and limitations. "
            "For each paper, extract the main contributions, methodological approaches, and technological innovations. "
            "Identify any limitations, gaps, or unanswered questions mentioned in the papers. "
            "Synthesize information across the papers to identify emerging trends, patterns, and contradictions. "
            "Be critical but fair in your assessment of the research. "
            "Focus on substantive insights rather than superficial details.\n\n"
            f"Here are the papers to analyze:\n{papers_str}"
        )

        # Define expected output format with schema example - USE TRIPLE QUOTES AND ESCAPE BRACES
        expected_output = """A JSON object summarizing key knowledge and limitations with this structure:
{{
  "key_findings": [
    {{
      "topic": "Topic Name",
      "findings": "Synthesized findings across papers",
      "papers": ["Paper Title 1", "Paper Title 2"]
    }},
    ...
  ],
  "methodologies": [
    {{
      "approach": "Methodology Name",
      "description": "Description of the methodology",
      "papers": ["Paper Title 1", "Paper Title 3"]
    }},
    ...
  ],
  "limitations": [
    {{
      "limitation": "Description of limitation or gap",
      "papers": ["Paper Title 2", "Paper Title 4"]
    }},
    ...
  ],
  "emerging_trends": [
    "Trend 1 description",
    "Trend 2 description",
    ...
  ]
}}
"""

        return Task(
            description=task_description,
            expected_output=expected_output,
            agent=agent,
            context=[],  # Use empty list like paper_finding_task
            async_execution=False
        )