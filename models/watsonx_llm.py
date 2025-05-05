from crewai import LLM

llm = LLM(
    model="watsonx/mistralai/mistral-large",
    max_tokens=1000,
    temperature=0
)