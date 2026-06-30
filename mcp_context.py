"""FastMCP Context helpers and compatibility patches."""

from __future__ import annotations

import asyncio
from typing import Literal

from fastmcp import Context
from fastmcp.utilities.logging import get_logger

logger = get_logger(__name__)


async def ctx_log(
    ctx: Context | None,
    level: Literal["debug", "info", "warning", "error"],
    message: str,
) -> None:
    """Send a log message to the MCP client without triggering unawaited coroutine warnings."""
    if ctx is None:
        return
    try:
        await ctx.request_context.session.send_log_message(level=level, data=message)
    except Exception:
        logger.debug("Failed to send MCP log message", exc_info=True)


async def ctx_info(ctx: Context | None, message: str) -> None:
    await ctx_log(ctx, "info", message)


async def ctx_warning(ctx: Context | None, message: str) -> None:
    await ctx_log(ctx, "warning", message)


async def ctx_error(ctx: Context | None, message: str) -> None:
    await ctx_log(ctx, "error", message)


def patch_fastmcp_context_logging() -> None:
    """Schedule MCP client log messages on the running event loop (fastmcp 0.4.x compat)."""

    def log(
        self: Context,
        level: Literal["debug", "info", "warning", "error"],
        message: str,
        *,
        logger_name: str | None = None,
    ) -> None:
        if self._request_context is None:
            return
        coro = self.request_context.session.send_log_message(
            level=level, data=message, logger=logger_name
        )
        try:
            asyncio.get_running_loop().create_task(coro)
        except RuntimeError:
            logger.debug("MCP log message dropped (no running event loop): %s", message)

    Context.log = log  # type: ignore[method-assign]
    Context.debug = lambda self, message, **extra: self.log("debug", message)  # type: ignore[method-assign, assignment]
    Context.info = lambda self, message, **extra: self.log("info", message)  # type: ignore[method-assign, assignment]
    Context.warning = lambda self, message, **extra: self.log("warning", message)  # type: ignore[method-assign, assignment]
    Context.error = lambda self, message, **extra: self.log("error", message)  # type: ignore[method-assign, assignment]
