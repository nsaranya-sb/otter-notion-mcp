# Otter.ai to Notion MCP Server (`otter-notion-mcp`)

An MCP (Model Context Protocol) server built using FastMCP that ingests exported **Otter.ai** transcripts (`.txt`, `.docx`) from Free or Paid Otter accounts, parses speaker timestamps, dialogue, and metadata, and formats structured payloads for creation in **Notion** via your existing Notion MCP connection.

## Architecture

```
[ Otter.ai (Free Export) ] 
       │
       ▼ (Save .txt / .docx)
[ ./transcripts/ Folder ] ──► [ otter-notion-mcp Server ] ──► [ Claude / Agent ] ──► [ Existing Notion MCP Server ] ──► [ Notion Workspace ]
```

## Features

- **Free Tier Compatible**: Works 100% with Otter Free plan exports (`.txt` or `.docx`).
- **Speaker & Timestamp Extraction**: Automatically parses speaker labels (e.g., `Sarah Chen [01:25]`) and utterance blocks.
- **Notion Summary Formatting**: Generates clean, structured markdown templates ready for Notion database pages.
- **Workflow Management**: Automatically moves processed transcripts into `./transcripts/processed/` to prevent duplicate imports.

## Quick Setup

1. **Clone & Setup Virtual Environment**:
   ```bash
   git clone https://github.com/nsaranya-sb/otter-notion-mcp.git
   cd otter-notion-mcp
   python3 -m venv .venv
   source .venv/bin/activate
   pip install "mcp<2.0.0" python-docx python-dotenv pytest
   ```

2. **Run Pytest Suite**:
   ```bash
   pytest tests/
   ```

3. **Smoke Test with Sample Transcript**:
   ```bash
   python3 test_client.py
   ```

## Wiring into Claude Code / Antigravity / Claude Desktop

Add `otter-notion-mcp` alongside your existing `notion` server in your MCP config (`.claude/mcp.json` or `mcp_config.json`):

```json
{
  "mcpServers": {
    "otter-notion-mcp": {
      "command": "/absolute/path/to/otter-notion-mcp/.venv/bin/python3",
      "args": ["/absolute/path/to/otter-notion-mcp/server.py"]
    },
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/mcp-server-notion"]
    }
  }
}
```

## End-to-End Workflow

1. Export any interview or meeting transcript from Otter.ai as `.txt` or `.docx` into `./transcripts/`.
2. In your chat session with Claude / Antigravity, give the command:

> *"Check `./transcripts/` for unprocessed Otter interview transcripts. Parse the candidate interview, summarize key discussion points, and create a page in my Notion 'Interviews' database using the Notion MCP server."*

3. The agent will call `list_unprocessed_transcripts` and `parse_otter_transcript` from `otter-notion-mcp`, summarize the content, call your Notion MCP server to create the page, and then invoke `mark_transcript_as_processed`.
