FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    TMPDIR=/dev/shm

RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv --python=python3.12 && \
    uv pip install vllm>=0.8.5

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH" \
    CC=gcc \
    CXX=g++

ENTRYPOINT [ "uv", "run" ]
