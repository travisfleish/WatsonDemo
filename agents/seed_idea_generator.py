from agents.base_agent import BaseAgent


class SeedIdeaGenerator:
    """Agent responsible for generating initial research ideas."""

    @staticmethod
    def create():
        return BaseAgent.create(
            name="Seed Idea Generator",
            role="Seed Idea Generator",
            goal="Generate initial research ideas by combining knowledge from related papers",
            backstory="You are an expert at combining knowledge from multiple "
                      "sources to generate novel research ideas.",
            tools=[]
        )