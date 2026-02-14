"""Brave Search API client."""

import os
from typing import Any

import aiohttp
from aiohttp import ClientError

from .api_models import SearchResult, WebSearchResponse


class APIError(Exception):
    """Brave Search API error."""

    def __init__(self, status: int, message: str, details: dict[str, Any] | None = None) -> None:
        self.status = status
        self.message = message
        self.details = details
        super().__init__(f"Brave Search API Error {status}: {message}")


class BraveSearchClient:
    """Async client for the Brave Search API."""

    BASE_URL = "https://api.search.brave.com/res/v1"

    def __init__(self, api_key: str | None = None, timeout: float = 30.0) -> None:
        self.api_key = api_key or os.environ.get("BRAVE_SEARCH_API_KEY")
        if not self.api_key:
            raise ValueError(
                "BRAVE_SEARCH_API_KEY is required. "
                "Get your API key from https://brave.com/search/api/"
            )
        self.timeout = timeout
        self._session: aiohttp.ClientSession | None = None

    async def _ensure_session(self) -> None:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers={
                    "Accept": "application/json",
                    "Accept-Encoding": "gzip",
                    "X-Subscription-Token": self.api_key or "",
                },
                timeout=aiohttp.ClientTimeout(total=self.timeout),
            )

    async def close(self) -> None:
        """Close the HTTP session."""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    async def search(
        self,
        query: str,
        count: int = 10,
        safesearch: str = "moderate",
        freshness: str | None = None,
        country: str = "us",
    ) -> WebSearchResponse:
        """Search the web using Brave Search.

        Args:
            query: Search query string.
            count: Number of results (max 20).
            safesearch: Filter level (off, moderate, strict).
            freshness: Time filter (pd, pw, pm, py).
            country: 2-letter country code.

        Returns:
            WebSearchResponse with results.
        """
        await self._ensure_session()
        assert self._session is not None

        params: dict[str, str] = {
            "q": query,
            "count": str(min(count, 20)),
            "safesearch": safesearch,
            "country": country,
        }
        if freshness:
            params["freshness"] = freshness

        try:
            async with self._session.get(f"{self.BASE_URL}/web/search", params=params) as response:
                data = await response.json()

                if response.status == 401:
                    raise APIError(401, "Invalid API key. Check your BRAVE_SEARCH_API_KEY.")
                if response.status == 429:
                    raise APIError(429, "Rate limit exceeded. Please wait before retrying.")
                if response.status >= 400:
                    msg = data.get("message", f"HTTP {response.status}")
                    raise APIError(response.status, msg, data)

                raw_results = data.get("web", {}).get("results", [])
                results = [
                    SearchResult(
                        position=i + 1,
                        title=r.get("title", ""),
                        url=r.get("url", ""),
                        description=r.get("description", ""),
                        age=r.get("age"),
                    )
                    for i, r in enumerate(raw_results)
                ]

                return WebSearchResponse(
                    query=query,
                    results=results,
                    total_results=len(results),
                )
        except ClientError as e:
            raise APIError(500, f"Network error: {e}") from e

    async def test_connection(self) -> dict[str, Any]:
        """Test the API connection with a simple search.

        Returns:
            Dict with success status and optional error.
        """
        try:
            result = await self.search("test", count=1)
            return {"success": True, "results": result.total_results}
        except APIError as e:
            return {"success": False, "error": e.message}
