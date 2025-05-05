from dotenv import load_dotenv
from crewai import Crew, Process
import json
import logging
import os
from pathlib import Path

# Import tasks
from tasks.paper_finding_task import PaperFindingTask
from tasks.paper_analysis_task import PaperAnalysisTask
from tasks.idea_generation_task import IdeaGenerationTask
from tasks.idea_refinement_task import IdeaRefinementTask
from tasks.proposal_development_task import ProposalDevelopmentTask

# Import utility functions
from utils.helpers import validate_json_output, save_research_proposal

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("research_proposal_generator.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main(input_paper, output_dir="output"):
    """
    Execute the research proposal generation workflow.

    Args:
        input_paper (str): The title of the input paper to base the research on
        output_dir (str): Directory to save the output proposals

    Returns:
        dict: The generated research proposals
    """
    logger.info(f"Starting research proposal generation for: {input_paper}")

    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Step 1: Create tasks with proper context passing
        paper_finding_task = PaperFindingTask.create(input_paper)

        # Step 2: Create crew with sequential process
        crew = Crew(
            agents=[
                paper_finding_task.agent
            ],
            tasks=[
                paper_finding_task
            ],
            process=Process.sequential,
            verbose=2
        )

        # Step 3: Execute the paper finding task
        logger.info("Executing paper finding task...")
        papers_result = crew.kickoff(inputs={"input_paper": input_paper})

        # Validate the papers result
        try:
            papers_data = validate_json_output(papers_result)
            logger.info(f"Found {len(papers_data)} related papers")
        except ValueError as e:
            logger.error(f"Invalid papers result: {str(e)}")
            logger.warning("Proceeding with raw paper finding result")
            papers_data = papers_result

        # Step 4: Paper analysis task
        paper_analysis_task = PaperAnalysisTask.create(papers_data)
        crew = Crew(
            agents=[paper_analysis_task.agent],
            tasks=[paper_analysis_task],
            process=Process.sequential,
            verbose=2
        )

        logger.info("Executing paper analysis task...")
        analysis_result = crew.kickoff()

        # Validate the analysis result
        try:
            analysis_data = validate_json_output(analysis_result)
            logger.info("Successfully analyzed papers")
        except ValueError as e:
            logger.error(f"Invalid analysis result: {str(e)}")
            logger.warning("Proceeding with raw analysis result")
            analysis_data = analysis_result

        # Step 5: Idea generation task
        idea_generation_task = IdeaGenerationTask.create(analysis_data)
        crew = Crew(
            agents=[idea_generation_task.agent],
            tasks=[idea_generation_task],
            process=Process.sequential,
            verbose=2
        )

        logger.info("Executing idea generation task...")
        ideas_result = crew.kickoff()

        # Validate the ideas result
        try:
            ideas_data = validate_json_output(ideas_result)
            logger.info(f"Generated {len(ideas_data)} research ideas")
        except ValueError as e:
            logger.error(f"Invalid ideas result: {str(e)}")
            logger.warning("Proceeding with raw ideas result")
            ideas_data = ideas_result

        # Step 6: Idea refinement task
        idea_refinement_task = IdeaRefinementTask.create(ideas_data)
        crew = Crew(
            agents=[idea_refinement_task.agent],
            tasks=[idea_refinement_task],
            process=Process.sequential,
            verbose=2
        )

        logger.info("Executing idea refinement task...")
        refined_ideas_result = crew.kickoff()

        # Validate the refined ideas result
        try:
            refined_ideas_data = validate_json_output(refined_ideas_result)
            logger.info(f"Refined {len(refined_ideas_data)} research ideas")
        except ValueError as e:
            logger.error(f"Invalid refined ideas result: {str(e)}")
            logger.warning("Proceeding with raw refined ideas result")
            refined_ideas_data = refined_ideas_result

        # Step 7: Proposal development task
        proposal_development_task = ProposalDevelopmentTask.create(refined_ideas_data)
        crew = Crew(
            agents=[proposal_development_task.agent],
            tasks=[proposal_development_task],
            process=Process.sequential,
            verbose=2
        )

        logger.info("Executing proposal development task...")
        proposals_result = crew.kickoff()

        # Step 8: Process and validate the final result
        try:
            proposals = validate_json_output(proposals_result)
            logger.info(f"Generated {len(proposals)} research proposals")

            # Save the proposals to disk
            for i, proposal in enumerate(proposals, 1):
                filepath = save_research_proposal(proposal, output_dir)
                logger.info(f"Saved proposal {i} to {filepath}")

            # Display summary information
            display_proposals_summary(proposals)

            return proposals

        except ValueError as e:
            logger.error(f"Error processing final result: {str(e)}")
            logger.warning("Returning raw result")
            print("Result was not in expected JSON format:")
            print(proposals_result)
            return proposals_result

    except Exception as e:
        logger.error(f"Error in research proposal generation: {str(e)}", exc_info=True)
        raise


def display_proposals_summary(proposals):
    """
    Display a summary of the generated research proposals.

    Args:
        proposals (list): List of research proposal dictionaries
    """
    print(f"\nGenerated {len(proposals)} research proposals:")

    for i, proposal in enumerate(proposals, 1):
        print(f"\nProposal {i}:")
        print(f"Title: {proposal.get('proposal_title', 'N/A')}")
        print(f"Methodology: {proposal.get('methodology', 'N/A')[:200]}...")
        print(f"Expected Outcomes: {proposal.get('expected_outcomes', 'N/A')[:200]}...")
        print("-" * 80)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate research proposals based on an input paper")
    parser.add_argument("paper_title", type=str, nargs="?",
                        default="Advanced Machine Learning Techniques for Scientific Discovery",
                        help="Title of the input paper to base research on")
    parser.add_argument("--output", "-o", type=str, default="output",
                        help="Directory to save output proposals")

    args = parser.parse_args()

    main(args.paper_title, args.output)