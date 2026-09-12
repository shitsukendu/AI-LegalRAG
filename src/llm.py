import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# Load environment variables
load_dotenv()


# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")


if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Please check your .env file."
    )


# Create Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.1,
    google_api_key=api_key
)


def ask_gemini(prompt):
    """
    Send a prompt to Gemini and return the response.
    """

    response = llm.invoke(prompt)

    return response.content