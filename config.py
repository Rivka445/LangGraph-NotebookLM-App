import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

LLM_MODEL = "gpt-4o-mini"
LLM_TEMPERATURE = 0.3
MAX_SEARCH_RESULTS = 5

SYSTEM_PROMPT = (
    "You are a professional research assistant. Your role is to gather high-quality sources from the internet. "
    "Present the final approved list clearly with source name, URL, and a brief description."
)
