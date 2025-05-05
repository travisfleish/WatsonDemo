from agents.base_agent import BaseAgent
from utils.helpers import load_prompt_template


class SeedIdeaGenerator(BaseAgent):
    """Agent responsible for generating initial research ideas."""

    @staticmethod
    def create():
        """
        Factory method to create a Seed Idea Generator agent.

        Returns:
            Agent: A configured CrewAI agent for generating research ideas
        """
        # Load the system prompt from templates
        system_prompt = load_prompt_template("seed_idea_generator")

        return BaseAgent.create(
            name="Seed Idea Generator",
            role="Seed Idea Generator",
            goal="Generate initial research ideas by combining knowledge from related papers",
            backstory="You are an expert at combining knowledge from multiple "
                      "sources to generate novel research ideas. You identify gaps "
                      "in existing research and propose creative solutions that "
                      "build upon established methodologies while exploring new directions.",
            tools=[],  # This agent primarily uses reasoning, no specific tools needed
            system_prompt=system_prompt,
            verbose=True
        )