"""
Standalone MCP client test for otter-notion-mcp server over stdio.

Run:
    .venv/bin/python3 test_client.py
"""
import asyncio
import json
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_PATH = os.path.join(os.path.dirname(__file__), "server.py")
SAMPLE_TRANSCRIPT = os.path.join(os.path.dirname(__file__), "transcripts", "sample_otter_interview.txt")


async def main():
    params = StdioServerParameters(command=sys.executable, args=[SERVER_PATH])

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("=== Tools exposed by otter-notion-mcp server ===")
            for t in tools.tools:
                print(f"- {t.name}: {t.description.strip().splitlines()[0]}")
            print()

            print("=== 1. Listing Unprocessed Transcripts ===")
            list_res = await session.call_tool("list_unprocessed_transcripts", arguments={})
            print(list_res.content[0].text)
            print()

            print("=== 2. Parsing Sample Otter Transcript ===")
            parse_res = await session.call_tool("parse_otter_transcript", arguments={"file_path": SAMPLE_TRANSCRIPT})
            data = json.loads(parse_res.content[0].text)
            print(f"Title: {data['title']}")
            print(f"Speakers Identified: {data['speakers']}")
            print(f"Utterance Count: {data['utterance_count']}")
            print("\n--- Notion Summary Markdown Payload ---")
            print(data['notion_summary_template'])


if __name__ == "__main__":
    asyncio.run(main())
