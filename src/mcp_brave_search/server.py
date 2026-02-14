"""Brave Search MCP Server - FastMCP Implementation."""

import logging
import os
import sys

from dotenv import load_dotenv
from fastmcp import Context, FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from .api_client import APIError, BraveSearchClient
from .api_models import WebSearchResponse

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("mcp_brave_search")

load_dotenv()

mcp = FastMCP("Brave Search")

_client: BraveSearchClient | None = None


def get_client() -> BraveSearchClient:
    """Get or create the Brave Search client."""
    global _client
    if _client is None:
        api_key = os.environ.get("BRAVE_SEARCH_API_KEY")
        if not api_key:
            raise ValueError(
                "BRAVE_SEARCH_API_KEY is required. "
                "Get your API key from https://brave.com/search/api/"
            )
        _client = BraveSearchClient(api_key=api_key)
    return _client


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    """Health check endpoint for monitoring."""
    return JSONResponse({"status": "healthy", "service": "mcp-brave-search"})


@mcp.tool()
async def web_search(
    query: str,
    count: int = 10,
    safesearch: str = "moderate",
    freshness: str | None = None,
    country: str = "us",
    ctx: Context | None = None,
) -> WebSearchResponse:
    """Search the web using Brave Search.

    Args:
        query: Search keywords or natural language question.
        count: Number of results to return (default: 10, max: 20).
        safesearch: Safe search filter level: "off", "moderate", or "strict" (default: "moderate").
        freshness: Time filter: "pd" (past day), "pw" (past week), "pm" (past month), "py" (past year).
        country: 2-letter country code (default: "us").
        ctx: MCP context.

    Returns:
        Search results with titles, URLs, and descriptions.
    """
    client = get_client()

    if ctx:
        await ctx.info(f"Searching Brave for: {query[:80]}...")

    try:
        return await client.search(
            query=query,
            count=count,
            safesearch=safesearch,
            freshness=freshness,
            country=country,
        )
    except APIError as e:
        if ctx:
            await ctx.error(f"Brave Search API error: {e.message}")
        raise


# ASGI entrypoint (nimbletools-core container deployment)
app = mcp.http_app()

# Stdio entrypoint (mpak / Claude Desktop)
if __name__ == "__main__":
    logger.info("Running in stdio mode")
    mcp.run()
