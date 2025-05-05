from crewai import Task
from agents.research_paper_finder import ResearchPaperFinder
import logging

logger = logging.getLogger(__name__)


class PaperFindingTask:
    """Task for finding relevant scientific papers."""

    @staticmethod
    def create(input_paper):
        """
        Create a task for finding relevant scientific papers.

        Args:
            input_paper (str): The title of the input paper to search for related papers

        Returns:
            Task: A configured CrewAI task
        """
        logger.info(f"Creating paper finding task for: {input_paper}")

        # Create the agent for this task
        agent = ResearchPaperFinder.create()

        # Create task description with specific instructions
        task_description = (
            f"Find 5-7 high-quality, recent scientific papers related to '{input_paper}' using web search. "
            f"Focus on papers published in the last 3 years from reputable sources. "
            f"Search for papers that explore different aspects of the topic and represent current research trends. "
            f"For each paper, extract the title, authors, publication year, venue, URL, and a brief summary. "
            f"Return your findings as a well-structured JSON list of papers."
        )

        # Define expected output format with schema example
        expected_output = (
            "A JSON list of papers with this structure:\n"
            "[\n"
            "  {\n"
            "    \"title\": \"Paper Title\",\n"
            "    \"authors\": \"Author1, Author2, ...\",\n"
            "    \"year\": 2023,\n"
            "    \"venue\": \"Journal/Conference Name\",\n"
            "    \"url\": \"https://paper-url.com\",\n"
            "    \"summary\": \"Brief summary of the paper's key contributions\"\n"
            "  },\n"
            "  ...\n"
            "]\n"
        )

        return Task(
            description=task_description,
            expected_output=expected_output,
            agent=agent,
            context=[],
            async_execution=False
        )