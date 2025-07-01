from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from agents.llm_provider import get_llm
from agents.tools import get_tools

def get_response_from_agent(
  model_provider: str,
  model_name: str,
  allow_search: bool,
  user_messages: list[str],
  system_prompt: str
) -> str:
  llm = get_llm(model_provider, model_name)
  tools = get_tools(allow_search)

  agent = create_react_agent(model=llm, tools=tools)

  state = {
    "messages": [
      SystemMessage(content=system_prompt),
      HumanMessage(content=user_messages[-1])
    ]
  }

  response = agent.invoke(state)
  messages = response.get("messages", [])

  ai_messages = [msg.content for msg in messages if isinstance(msg, AIMessage)]
  return ai_messages[-1] if ai_messages else "No response from AI"
