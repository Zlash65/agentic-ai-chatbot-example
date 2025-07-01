from fastapi import APIRouter
from backend.schema import ChatRequest
from agents.ai_agent import get_response_from_agent

router = APIRouter()

ALLOWED_PROVIDERS = ["groq", "gemini"]
ALLOWED_MODELS = ["llama-3.1-8b-instant", "llama3-70b-8192", "gemini-2.0-flash", "gemini-2.5-flash"]

@router.post("/chat")
def chat(request: ChatRequest):
  model_provider = request.model_provider.lower()
  model_name = request.model_name
  allow_search = request.allow_search

  if model_provider not in ALLOWED_PROVIDERS:
    raise ValueError(f"Invalid model provider: {request.model_provider}. Must be one of {ALLOWED_PROVIDERS}.")
  if model_name not in ALLOWED_MODELS:
    raise ValueError(f"Invalid model name: {model_name}. Must be one of {ALLOWED_MODELS}.")

  response = get_response_from_agent(
    model_provider=model_provider,
    model_name=model_name,
    allow_search=allow_search,
    user_messages=request.messages,
    system_prompt=request.system_prompt
  )

  return { "response": response }
