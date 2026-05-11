"""Directly run GitCodeMCP."""

from gitcode_api.llm.mcp import GitCodeMCP

if __name__ == "__main__":
    GitCodeMCP().mcp.run(show_banner=False)
