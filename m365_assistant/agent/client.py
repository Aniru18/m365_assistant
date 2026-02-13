import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def get_executor_llm():
    """
    GPT-style model responsible for:
    - Calling MCP tools
    - Fetching emails
    - Fetching calendar data
    - Returning structured JSON context
    """
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="openai/gpt-oss-120b",
        temperature=0,
    )


def get_planner_llm():
    """
    LLaMA model responsible for:
    - Creating prioritized daily routine
    - Strategic time blocking
    - Productivity optimization
    """
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.3-70b-versatile",
        temperature=0.3,
    )
