from langchain_community.tools.tavily_search import TavilySearchResults


def get_tools(allow_search: bool):
  tools = []
  if allow_search:
    tools.append(TavilySearchResults())

  return tools
