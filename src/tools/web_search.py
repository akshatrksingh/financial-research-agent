"""Tavily web search tool."""
from tavily import TavilyClient
from src.config import TAVILY_API_KEY
from typing import List, Dict

def search_web(query: str, max_results: int = 5) -> List[Dict]:
    """Search the web using Tavily.
    
    Args:
        query: Search query
        max_results: Number of results to return
        
    Returns:
        List of search results with title, url, snippet
    """
    try:
        client = TavilyClient(api_key=TAVILY_API_KEY)
        response = client.search(query, max_results=max_results)
        
        results = []
        for item in response.get("results", []):
            results.append({
                "title": item.get("title"),
                "url": item.get("url"),
                "snippet": item.get("content", "")[:200]  # First 200 chars
            })
        
        return results
    except Exception as e:
        return [{"error": str(e)}]

if __name__ == "__main__":
    # Test
    results = search_web("NVIDIA stock news")
    for r in results:
        print(f"{r['title']}: {r['snippet']}")