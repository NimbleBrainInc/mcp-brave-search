"""Pydantic models for Brave Search MCP Server responses."""

from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    """A single web search result."""

    position: int = Field(..., description="Position in search results")
    title: str = Field(..., description="Page title")
    url: str = Field(..., description="Page URL")
    description: str = Field("", description="Page description snippet")
    age: str | None = Field(None, description="How old the result is (e.g. '2 days ago')")


class WebSearchResponse(BaseModel):
    """Response model for web_search tool."""

    query: str = Field(..., description="The original search query")
    results: list[SearchResult] = Field(default_factory=list, description="Search results")
    total_results: int = Field(0, description="Number of results returned")
