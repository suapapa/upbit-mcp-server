"""MCP server-side request logging."""

from __future__ import annotations

from typing import Any

from fastmcp import FastMCP
from fastmcp.utilities.logging import get_logger

logger = get_logger(__name__)


def install_tool_call_logging(mcp: FastMCP) -> None:
    original_call_tool = mcp.call_tool

    async def call_tool_with_logging(name: str, arguments: dict[str, Any]):
        logger.info("CallToolRequest: tool=%s arguments=%s", name, arguments)
        return await original_call_tool(name, arguments)

    mcp.call_tool = call_tool_with_logging  # type: ignore[method-assign]
    mcp._mcp_server.call_tool()(call_tool_with_logging)
