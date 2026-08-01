"""
Unit tests for Otter.ai transcript parser.
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import parser


def test_parse_transcript_file_txt(tmp_path):
    sample_file = tmp_path / "interview_test.txt"
    sample_file.write_text(
        "Candidate Interview: Alex Morgan\n\n"
        "Interviewer 00:05\n"
        "Tell me about your Python background.\n\n"
        "Alex Morgan 00:15\n"
        "I have 5 years of experience building Python FastMCP servers.\n"
    )

    res = parser.parse_transcript_file(str(sample_file))

    assert res["title"] == "Candidate Interview: Alex Morgan"
    assert "Alex Morgan" in res["speakers"]
    assert "Interviewer" in res["speakers"]
    assert res["utterance_count"] == 2
    assert "FastMCP" in res["notion_summary_template"]


def test_parse_missing_file_raises_error():
    with pytest.raises(FileNotFoundError):
        parser.parse_transcript_file("non_existent_file.txt")
