from dotenv import load_dotenv
from crewai import Crew, Process
import json

# Import tasks
from tasks.paper_finding_task import PaperFindingTask
from tasks.paper_analysis_task import PaperAnalysisTask
from tasks.idea_generation_task import IdeaGenerationTask
from tasks.idea_refinement_task import IdeaRefinementTask
from tasks.proposal_development_task import ProposalDevelopmentTask

# Load environment variables
load_dotenv()


def main(input_paper):
    """
    Execute the research proposal generation workflow.

    Args:
        input_paper: The title of the input paper to base the research on
    """
    # Create tasks
    paper_finding_task = PaperFindingTask.create(input_paper)
    paper_analysis_task = PaperAnalysisTask.create()
    idea_generation_task = IdeaGenerationTask.create()
    idea_refinement_task = IdeaRefinementTask.create()
    proposal_development_task = ProposalDevelopmentTask.create()

    # Create crew
    crew = Crew(
        tasks=[
            paper_finding_task,
            paper_analysis_task,
            idea_generation_task,
            idea_refinement_task,
            proposal_development_task
        ],
        process=Process.sequential,
        verbose=2
    )

    # Execute the workflow
    result = crew.kickoff(inputs={"input_paper": input_paper})

    # Process and display the result
    try:
        proposals = json.loads(result)
        print(f"Generated {len(proposals)} research proposals:")
        for i, proposal in enumerate(proposals, 1):
            print(f"\nProposal {i}:")
            print(f"Title: {proposal.get('proposal_title', 'N/A')}")
            print(f"Methodology: {proposal.get('methodology', 'N/A')}")
            print(f"Expected Outcomes: {proposal.get('expected_outcomes', 'N/A')}")
    except json.JSONDecodeError:
        print("Result was not in expected JSON format:")
        print(result)

    return result


if __name__ == "__main__":
    example_paper = "Advanced Machine Learning Techniques for Scientific Discovery"
    main(example_paper)