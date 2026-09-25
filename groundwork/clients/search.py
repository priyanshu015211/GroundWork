"""Thin Tavily search client wrapper used by GroundWork researchers."""

from tavily import TavilyClient

from groundwork.config import Settings
from groundwork.models import Source


class SearchClient:
    def __init__(self, settings: Settings) -> None:
        if not settings.tavily_api_key:
            raise ValueError("Tavily API key is required to initialize SearchClient.")
        self._client = TavilyClient(api_key=settings.tavily_api_key)

    def search(self, query: str, *, max_results: int = 5) -> list[Source]:
        if not query.strip():
            raise ValueError("query cannot be empty.")
        if max_results < 1:
            raise ValueError("max_results must be >= 1.")

        response = self._client.search(query=query, max_results=max_results)
        results = response.get("results", []) if isinstance(response, dict) else []

        return [
            Source(
                url=item.get("url", ""),
                title=item.get("title", "Untitled source"),
                snippet=item.get("content", ""),
            )
            for item in results
            if item.get("url")
        ]
