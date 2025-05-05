from agents.base_agent import BaseAgent


class ResearchProposalDeveloper:
    """Agent responsible for developing comprehensive research proposals."""

    @staticmethod
    def create():
        return BaseAgent.create(
            name="Research Proposal Developer",
            role="Research Proposal Developer",
            goal="Transform ideas into complete research proposals",
            backstory="You are an expert at structuring comprehensive research "
                      "proposals with clear methodologies and expected goals.",
            tools=[]
        )