"""
Configuration settings for the research proposal generation system.
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
PROMPTS_DIR = BASE_DIR / "prompts"

# API Configurations
WATSONX_APIKEY = os.getenv("WATSONX_APIKEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
WATSONX_URL = os.getenv("WATSONX_URL")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# LLM Settings
LLM_MODEL = "watsonx/mistralai/mistral-large"
LLM_MAX_TOKENS = 1000
LLM_TEMPERATURE = 0
LLM_TOP_P = 1.0
LLM_TOP_K = 50

# Agent Settings
AGENT_VERBOSE = True

# Task Settings
TASK_ASYNC_EXECUTION = False

# Search Settings
SEARCH_MAX_RESULTS = 5
SEARCH_MAX_PAGES = 3

# Web Scraping Settings
SCRAPE_TIMEOUT = 30  # seconds
SCRAPE_MAX_RETRIES = 3
SCRAPE_USER_AGENT = "Research Proposal Generator Bot"

# Output Settings
JSON_OUTPUT_INDENT = 2

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = BASE_DIR / "logs" / "app.log"

# Debug mode
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")