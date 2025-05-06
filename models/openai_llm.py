# models/openai_llm.py
import os
import logging
from crewai import LLM

logger = logging.getLogger(__name__)

# Check for API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.warning("OpenAI API key not found in environment variables. Make sure to set OPENAI_API_KEY.")

try:
    # Initialize the OpenAI LLM - IMPORTANT: Do NOT use the 'provider' parameter
    llm = LLM(
        model="gpt-4o",  # You can also use "gpt-3.5-turbo" for a more cost-effective option
        api_key=api_key,
        temperature=0
    )
    logger.info(f"Successfully initialized OpenAI LLM")

except Exception as e:
    logger.error(f"Error initializing OpenAI LLM: {str(e)}")


    # Define a fallback that will raise a clear error if used
    class FallbackLLM:
        def __call__(self, *args, **kwargs):
            raise RuntimeError("OpenAI LLM initialization failed. Please check your API key.")


    llm = FallbackLLM()