from agents.base_agent import BaseAgent
from utils.helpers import load_prompt_template


class IdeaRefinementSpecialist(BaseAgent):
    """Agent responsible for refining and enhancing research ideas."""

    @staticmethod
    def create():
        """
        Factory method to create an Idea Refinement Specialist agent.

        Returns:
            Agent: A configured CrewAI agent for refining research ideas
        """
        # Load the system prompt from templates
        system_prompt = load_prompt_template("idea_refinement_specialist")

        return BaseAgent.create(
            name="Idea Refinement Specialist",
            role="Idea Refinement Specialist",
            goal="Refine and enhance generated research ideas",
            backstory="You are an expert at improving research ideas "
                      "through critical analysis and strategic enhancement. "
                      "You evaluate ideas for scientific merit, feasibility, "
                      "and potential impact, then provide concrete suggestions "
                      "for strengthening each concept.",
            tools=[],  # This agent primarily uses reasoning, no specific tools needed
            system_prompt=system_prompt,
            verbose=True
        )