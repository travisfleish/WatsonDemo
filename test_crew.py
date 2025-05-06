"""
Test script for verifying CrewAI tools compatibility.
"""
import os
import logging
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

# Import our tools
from tools.tavily_search import tavily_search
from tools.scrape_website import scrape_website

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def main():
    """Run a simple test of the tools"""
    logger.info("Testing CrewAI tools")

    # Verify that OPENAI_API_KEY is set
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("OPENAI_API_KEY environment variable is not set!")
        logger.info("Please create a .env file with your OPENAI_API_KEY")
        return "Error: OPENAI_API_KEY not set"

    # Create a researcher agent with both tools
    researcher = Agent(
        name="Researcher",
        role="Research Specialist",
        goal="Find and analyze information on various topics",
        backstory="You are an expert researcher with years of experience finding accurate information.",
        tools=[tavily_search, scrape_website],
        verbose=True
    )

    # Create a task that uses both tools
    research_task = Task(
        description=(
            "Research the topic of 'artificial intelligence ethics' and provide a summary. "
            "Use the search tool to find information, and the scrape tool to analyze any relevant websites."
        ),
        expected_output="A summary of findings about AI ethics",
        agent=researcher
    )

    # Create a crew with the agent and task
    crew = Crew(
        agents=[researcher],
        tasks=[research_task],
        process=Process.sequential,
        verbose=True
    )

    # Run the crew
    logger.info("Running test...")

    try:
        result = crew.kickoff()
        logger.info("\n=== TEST RESULT ===")
        logger.info(result)
        return result
    except Exception as e:
        logger.error(f"Error running crew: {str(e)}")
        return f"Error: {str(e)}"

if __name__ == "__main__":
    main()