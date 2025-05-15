FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    TMPDIR=/dev/shm
    
RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv --python=python3.12 && \
    uv pip install vllm>=0.8.5

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
ENTRYPOINT [ "uv", "run" ]