FROM python:3.10-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Enable bytecode compilation and python paths
ENV UV_COMPILE_BYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

# Copy configuration files
COPY pyproject.toml uv.lock* ./

# Install dependencies first (leverage Docker cache)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# Copy application source code
COPY main.py config.py sse_auth.py upbit_client.py ./
COPY tools/ ./tools/
COPY prompts/ ./prompts/
COPY resources/ ./resources/

# Sync project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# use `--env-file .env` instead
# ENV UPBIT_ACCESS_KEY=""
# ENV UPBIT_SECRET_KEY=""
# ENV UPBIT_MCP_SSE_TOKEN=""

EXPOSE 8000

CMD ["python", "main.py", "--transport", "sse"]
