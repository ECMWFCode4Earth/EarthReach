FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \ 
    UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install vllm>=0.8.5

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT [ "uv", "run" ]