# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.12
FROM ghcr.io/astral-sh/uv:python${PYTHON_VERSION}-bookworm-slim AS base

ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1

WORKDIR /app

# Copy only dependency manifests first so Docker can cache this layer
COPY pyproject.toml ./

# Generates uv.lock during the build and installs dependencies.
# If you commit uv.lock and want reproducible installs instead, copy it in
# above and use `RUN uv sync --frozen` here.
RUN uv sync

# Now copy the actual application code
COPY agent.py ./

# Pre-download model files (e.g. Silero VAD weights) so cold start doesn't
# fetch them on first job — LiveKit agents support a "download-files" step
RUN uv run agent.py download-files

CMD ["uv", "run", "agent.py", "start"]