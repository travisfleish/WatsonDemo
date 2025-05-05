from agents.base_agent import BaseAgent


class IdeaRefinementSpecialist:
    """Agent responsible for refining and enhancing research ideas."""

    @staticmethod
    def create():
        return BaseAgent.create(
            name="Idea Refinement Specialist",
            role="Idea Refinement Specialist",
            goal="Refine and enhance generated research ideas",
            backstory="You are an expert at improving research ideas "
                      "through iteration and improvement.",
            tools=[]
        )