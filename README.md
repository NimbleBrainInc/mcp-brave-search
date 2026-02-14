# Brave Search MCP Server

[![mpak](https://img.shields.io/badge/mpak-registry-blue)](https://mpak.dev/packages/@nimblebraininc/brave-search?utm_source=github&utm_medium=readme&utm_campaign=mcp-brave-search)
[![NimbleBrain](https://img.shields.io/badge/NimbleBrain-nimblebrain.ai-purple)](https://nimblebrain.ai?utm_source=github&utm_medium=readme&utm_campaign=mcp-brave-search)
[![Discord](https://img.shields.io/badge/Discord-community-5865F2)](https://nimblebrain.ai/discord?utm_source=github&utm_medium=readme&utm_campaign=mcp-brave-search)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A [Model Context Protocol](https://modelcontextprotocol.io) (MCP) server that provides web search capabilities using the [Brave Search API](https://brave.com/search/api/). Search the web from any MCP client with support for safe search, freshness filters, and country-specific results.

**[View on mpak registry](https://mpak.dev/packages/@nimblebraininc/brave-search?utm_source=github&utm_medium=readme&utm_campaign=mcp-brave-search)** | **Built by [NimbleBrain](https://nimblebrain.ai?utm_source=github&utm_medium=readme&utm_campaign=mcp-brave-search)**

## Install

Install with [mpak](https://mpak.dev?utm_source=github&utm_medium=readme&utm_campaign=mcp-brave-search):

```bash
mpak install @nimblebraininc/brave-search
```

### Configuration

Get your API key from [Brave Search API](https://brave.com/search/api/), then configure:

```bash
mpak config set @nimblebraininc/brave-search api_key YOUR_API_KEY
```

### Claude Code

```bash
claude mcp add brave-search -- mpak run @nimblebraininc/brave-search
```

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "brave-search": {
      "command": "mpak",
      "args": ["run", "@nimblebraininc/brave-search"]
    }
  }
}
```

See the [mpak registry page](https://mpak.dev/packages/@nimblebraininc/brave-search?utm_source=github&utm_medium=readme&utm_campaign=mcp-brave-search) for full install options.

## Tools

### web_search

Search the web using Brave Search. Returns relevant web pages with titles, URLs, descriptions, and age.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | `string` | Yes | Search keywords or natural language question |
| `count` | `integer` | No | Number of results to return, max 20 (default: `10`) |
| `safesearch` | `string` | No | Filter level: `"off"`, `"moderate"`, `"strict"` (default: `"moderate"`) |
| `freshness` | `string` | No | Time filter: `"pd"` (day), `"pw"` (week), `"pm"` (month), `"py"` (year) |
| `country` | `string` | No | 2-letter country code (default: `"us"`) |

**Example call:**

```json
{
  "name": "web_search",
  "arguments": {
    "query": "Model Context Protocol",
    "count": 5,
    "freshness": "pw"
  }
}
```

**Example response:**

```json
{
  "query": "Model Context Protocol",
  "results": [
    {
      "position": 1,
      "title": "Model Context Protocol",
      "url": "https://modelcontextprotocol.io",
      "description": "The Model Context Protocol is an open standard...",
      "age": "3 days ago"
    }
  ],
  "total_results": 5
}
```

## Quick Start

### Local Development

```bash
git clone https://github.com/NimbleBrainInc/mcp-brave-search.git
cd mcp-brave-search

# Install dependencies
uv sync

# Set API key
cp .env.example .env
# Edit .env with your API key

# Run the server (stdio mode)
uv run python -m mcp_brave_search.server
```

The server supports HTTP transport with:
- Health check: `GET /health`
- MCP endpoint: `POST /mcp`

## Development

```bash
# Install with dev dependencies
uv sync --group dev

# Run all checks (format, lint, typecheck, unit tests)
make check

# Run unit tests
make test

# Run with coverage
make test-cov
```

## About

Brave Search MCP Server is published on the [mpak registry](https://mpak.dev?utm_source=github&utm_medium=readme&utm_campaign=mcp-brave-search) and built by [NimbleBrain](https://nimblebrain.ai?utm_source=github&utm_medium=readme&utm_campaign=mcp-brave-search). mpak is an open registry for [Model Context Protocol](https://modelcontextprotocol.io) servers.

- [mpak registry](https://mpak.dev?utm_source=github&utm_medium=readme&utm_campaign=mcp-brave-search)
- [NimbleBrain](https://nimblebrain.ai?utm_source=github&utm_medium=readme&utm_campaign=mcp-brave-search)
- [MCP specification](https://modelcontextprotocol.io)
- [Discord community](https://nimblebrain.ai/discord?utm_source=github&utm_medium=readme&utm_campaign=mcp-brave-search)

## License

MIT
