# syntax=docker/dockerfile:1.7

# Pinned uv image — tag only, not digest. For stricter supply-chain control,
# replace with `ghcr.io/astral-sh/uv:0.11.7@sha256:<digest>`.
FROM ghcr.io/astral-sh/uv:0.11.7 AS uv

FROM python:3.13-slim

ENV PYTHONNOUSERSITE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Copy uv binaries from the pinned image above.
COPY --from=uv /uv /uvx /bin/

WORKDIR /app/user_agent

# Install dependencies in their own layer so code changes don't invalidate
# the dep-install cache on every rebuild.
COPY pyproject.toml uv.lock uv.toml ./
RUN uv sync --frozen --no-dev --no-install-project

# Copy the rest of the application source.
COPY . .

# Precompile Python bytecode at build time so cold starts don't pay for it.
# These base images ship almost none of the standard library precompiled
# (~2% of stdlib .py files, on both Debian-slim and Azure Linux), so without
# this every new container recompiles hundreds of stdlib modules on first
# import. Dependencies are best-effort (`|| true`) so a stray unparsable file
# vendored by a third-party package can't fail the build; application code is
# compiled strictly so a syntax error surfaces at build time rather than at
# container start.
# PYTHONDONTWRITEBYTECODE is cleared for these commands only: it blocks
# bytecode *writes*, not *reads*, so images that set it still benefit.
RUN PYTHONDONTWRITEBYTECODE= .venv/bin/python -m compileall -q $(.venv/bin/python -c "import sysconfig as s; print(s.get_paths()['stdlib'], s.get_paths()['purelib'])") || true; \
    PYTHONDONTWRITEBYTECODE= .venv/bin/python -m compileall -q -x '[.]venv' .

# Create an unprivileged user and hand over ownership of the app tree.
# Running as root in a container is a privilege-escalation risk if a process
# escapes the sandbox; nothing in this agent needs root.
RUN groupadd --system app && \
    useradd  --system --gid app --home-dir /app --shell /sbin/nologin appuser && \
    chown -R appuser:app /app
USER appuser

EXPOSE 8088

# Simple liveness probe — the Responses host serves on :8088. If the TCP
# port is open the container is considered healthy; adjust to hit a real
# /health endpoint once the hosting layer exposes one.
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import socket,sys; s=socket.socket(); s.settimeout(2); \
                   sys.exit(0) if s.connect_ex(('127.0.0.1',8088))==0 else sys.exit(1)"

CMD ["/app/user_agent/.venv/bin/python", "main.py"]
