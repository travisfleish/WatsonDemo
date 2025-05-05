from agents.base_agent import BaseAgent
from utils.helpers import load_prompt_template


class ResearchProposalDeveloper(BaseAgent):
    """Agent responsible for developing comprehensive research proposals."""

    @staticmethod
    def create():
        """
        Factory method to create a Research Proposal Developer agent.

        Returns:
            Agent: A configured CrewAI agent for developing research proposals
        """
        # Load the system prompt from templates
        system_prompt = load_prompt_template("research_proposal_developer")

        return BaseAgent.create(
            name="Research Proposal Developer",
            role="Research Proposal Developer",
            goal="Transform ideas into complete research proposals",
            backstory="You are an expert at structuring comprehensive research "
                      "proposals with clear methodologies and expected goals. "
                      "You excel at developing formal research plans with "
                      "detailed objectives, methodologies, expected outcomes, "
                      "and resource requirements.",
            tools=[],  # This agent primarily uses reasoning, no specific tools needed
            system_prompt=system_prompt,
            verbose=True
        )