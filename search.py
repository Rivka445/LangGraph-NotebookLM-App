from tavily import TavilyClient
from config import TAVILY_API_KEY, MAX_SEARCH_RESULTS


def fetch_sources(topic: str) -> list[dict]:
    client = TavilyClient(api_key=TAVILY_API_KEY)
    response = client.search(topic, max_results=MAX_SEARCH_RESULTS)
    return response.get("results", [])
