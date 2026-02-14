"""Unit tests for the Brave Search MCP server."""

from unittest.mock import AsyncMock, patch

import pytest
from fastmcp import Client

from mcp_brave_search.api_models import SearchResult, WebSearchResponse
from mcp_brave_search.server import mcp


@pytest.fixture
def mock_response() -> WebSearchResponse:
    """Create a mock search response."""
    return WebSearchResponse(
        query="test query",
        results=[
            SearchResult(
                position=1,
                title="Test Result",
                url="https://example.com",
                description="A test result description",
                age="2 days ago",
            ),
            SearchResult(
                position=2,
                title="Another Result",
                url="https://example.org",
                description="Another description",
                age=None,
            ),
        ],
        total_results=2,
    )


@pytest.mark.asyncio
async def test_tools_list() -> None:
    """Test that tools are properly registered."""
    async with Client(mcp) as client:
        tools = await client.list_tools()

        assert len(tools) == 1
        tool_names = [tool.name for tool in tools]
        assert "web_search" in tool_names


@pytest.mark.asyncio
async def test_web_search_tool(mock_response: WebSearchResponse) -> None:
    """Test web_search tool returns results."""
    with patch("mcp_brave_search.server.get_client") as mock_get_client:
        mock_client = AsyncMock()
        mock_client.search.return_value = mock_response
        mock_get_client.return_value = mock_client

        async with Client(mcp) as client:
            result = await client.call_tool("web_search", {"query": "test query"})

        mock_client.search.assert_called_once_with(
            query="test query",
            count=10,
            safesearch="moderate",
            freshness=None,
            country="us",
        )
        assert result is not None


@pytest.mark.asyncio
async def test_web_search_with_params(mock_response: WebSearchResponse) -> None:
    """Test web_search tool with all parameters."""
    with patch("mcp_brave_search.server.get_client") as mock_get_client:
        mock_client = AsyncMock()
        mock_client.search.return_value = mock_response
        mock_get_client.return_value = mock_client

        async with Client(mcp) as client:
            await client.call_tool(
                "web_search",
                {
                    "query": "test",
                    "count": 5,
                    "safesearch": "strict",
                    "freshness": "pw",
                    "country": "gb",
                },
            )

        mock_client.search.assert_called_once_with(
            query="test",
            count=5,
            safesearch="strict",
            freshness="pw",
            country="gb",
        )


def test_search_result_model() -> None:
    """Test SearchResult model creation."""
    result = SearchResult(
        position=1,
        title="Test",
        url="https://example.com",
        description="A description",
        age="1 day ago",
    )
    assert result.position == 1
    assert result.title == "Test"
    assert result.url == "https://example.com"
    assert result.age == "1 day ago"


def test_web_search_response_model() -> None:
    """Test WebSearchResponse model creation."""
    response = WebSearchResponse(
        query="test",
        results=[],
        total_results=0,
    )
    assert response.query == "test"
    assert response.results == []
    assert response.total_results == 0
