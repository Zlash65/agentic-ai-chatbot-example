from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.config import GROQ_API_KEY, GOOGLE_API_KEY

def get_llm(model_provider: str, model_name: str):
  if model_provider == "groq":
    if not GROQ_API_KEY:
      raise ValueError("GROQ_API_KEY is not set")
    return ChatGroq(model=model_name, api_key=GROQ_API_KEY)

  elif model_provider == "gemini":
    if not GOOGLE_API_KEY:
      raise ValueError("GOOGLE_API_KEY is not set")
    return ChatGoogleGenerativeAI(model=model_name, api_key=GOOGLE_API_KEY)

  else:
    raise ValueError(f"Invalid model provider: {model_provider}")
