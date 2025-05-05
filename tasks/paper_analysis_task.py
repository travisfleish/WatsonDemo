from crewai import Task
from agents.research_paper_analyst import ResearchPaperAnalyst
import logging

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

        # Create task description with specific instructions
        task_description = (
            "Analyze the related papers to identify key knowledge, methodologies, and limitations. "
            "For each paper, extract the main contributions, methodological approaches, and technological innovations. "
            "Identify any limitations, gaps, or unanswered questions mentioned in the papers. "
            "Synthesize information across the papers to identify emerging trends, patterns, and contradictions. "
            "Be critical but fair in your assessment of the research. "
            "Focus on substantive insights rather than superficial details."
        )

        # Define expected output format with schema example
        expected_output = (
            "A JSON object summarizing key knowledge and limitations with this structure:\n"
            "{\n"
            "  \"key_findings\": [\n"
            "    {\n"
            "      \"topic\": \"Topic Name\",\n"
            "      \"findings\": \"Synthesized findings across papers\",\n"
            "      \"papers\": [\"Paper Title 1\", \"Paper Title 2\"]\n"
            "    },\n"
            "    ...\n"
            "  ],\n"
            "  \"methodologies\": [\n"
            "    {\n"
            "      \"approach\": \"Methodology Name\",\n"
            "      \"description\": \"Description of the methodology\",\n"
            "      \"papers\": [\"Paper Title 1\", \"Paper Title 3\"]\n"
            "    },\n"
            "    ...\n"
            "  ],\n"
            "  \"limitations\": [\n"
            "    {\n"
            "      \"limitation\": \"Description of limitation or gap\",\n"
            "      \"papers\": [\"Paper Title 2\", \"Paper Title 4\"]\n"
            "    },\n"
            "    ...\n"
            "  ],\n"
            "  \"emerging_trends\": [\n"
            "    \"Trend 1 description\",\n"
            "    \"Trend 2 description\",\n"
            "    ...\n"
            "  ]\n"
            "}\n"
        )

        return Task(
            description=task_description,
            expected_output=expected_output,
            agent=agent,
            context=[research_papers] if research_papers else [],
            async_execution=False
        )