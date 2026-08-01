"""
Otter.ai to Notion MCP Server (FastMCP)

Exposes tools for Claude Code / Antigravity to ingest exported Otter.ai transcripts (.txt / .docx),
parse speakers and timestamps, and format structured summaries for Notion creation.
"""
import os
import shutil
from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP
import parser

mcp = FastMCP("otter-notion-mcp")


@mcp.tool()
def list_unprocessed_transcripts(folder_path: str = "./transcripts") -> Dict[str, Any]:
    """
    List all pending/unprocessed Otter.ai exported transcript files (.txt, .docx) in the folder.

    Args:
        folder_path: Path to the local folder containing exported Otter transcripts (default: './transcripts').
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)

    processed_dir = os.path.join(folder_path, "processed")
    os.makedirs(processed_dir, exist_ok=True)

    unprocessed_files = []
    for f in os.listdir(folder_path):
        full_path = os.path.join(folder_path, f)
        if os.path.isfile(full_path) and f.lower().endswith((".txt", ".docx", ".md")):
            unprocessed_files.append({
                "filename": f,
                "file_path": os.path.abspath(full_path),
                "size_bytes": os.path.getsize(full_path),
            })

    return {
        "folder_path": os.path.abspath(folder_path),
        "total_unprocessed": len(unprocessed_files),
        "files": unprocessed_files,
    }


@mcp.tool()
def parse_otter_transcript(file_path: str) -> Dict[str, Any]:
    """
    Parse an exported Otter.ai transcript file (.txt or .docx).
    Extracts speakers, timestamps, clean raw dialogue, and a structured markdown payload ready for Notion page creation.

    Args:
        file_path: Absolute or relative path to the transcript file.
    """
    return parser.parse_transcript_file(file_path)


@mcp.tool()
def mark_transcript_as_processed(file_path: str) -> Dict[str, Any]:
    """
    Move a transcript file to the './transcripts/processed' directory after successfully creating its Notion page.

    Args:
        file_path: Absolute or relative path to the processed transcript file.
    """
    if not os.path.exists(file_path):
        return {"status": "ERROR", "message": f"File '{file_path}' does not exist."}

    dir_name = os.path.dirname(file_path)
    filename = os.path.basename(file_path)

    processed_dir = os.path.join(dir_name, "processed")
    os.makedirs(processed_dir, exist_ok=True)

    dest_path = os.path.join(processed_dir, filename)
    shutil.move(file_path, dest_path)

    return {
        "status": "PROCESSED_AND_MOVED",
        "original_path": file_path,
        "new_path": os.path.abspath(dest_path),
    }


if __name__ == "__main__":
    mcp.run()
