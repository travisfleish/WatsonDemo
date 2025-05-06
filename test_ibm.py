# test_openai.py
from dotenv import load_dotenv
from models.openai_llm import llm

# Load environment variables
load_dotenv()

def test_openai_connection():
    """Test if the OpenAI LLM is working properly."""
    try:
        # A simple test message
        response = llm("Hello, can you hear me?")
        print("Connection successful!")
        print(f"Response: {response}")
        return True
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_openai_connection()