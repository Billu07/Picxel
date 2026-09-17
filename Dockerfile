# syntax=docker/dockerfile:1
# Picxel container: build CSS → install dependencies → slim, non-root runtime.

ARG PYTHON_IMAGE=python:3.12-slim
ARG UV_IMAGE=ghcr.io/astral-sh/uv:0.12.13

FROM ${UV_IMAGE} AS uv

# ---- 1. Stylesheet: Tailwind standalone CLI (no Node) ------------------------------------------
FROM ${PYTHON_IMAGE} AS assets
COPY --from=uv /uv /usr/local/bin/uv
WORKDIR /srv/picxel
ENV UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=never
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --only-group assets --no-install-project
COPY app ./app
RUN uv run --no-sync python -m app.cli css

# ---- 2. Python dependencies ---------------------------------------------------------------------
FROM ${PYTHON_IMAGE} AS builder
COPY --from=uv /uv /usr/local/bin/uv
WORKDIR /srv/picxel
ENV UV_LINK_MODE=copy UV_COMPILE_BYTECODE=1 UV_PYTHON_DOWNLOADS=never
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-default-groups --no-install-project
COPY README.md LICENSE ./
COPY app ./app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-default-groups

# ---- 3. Runtime ---------------------------------------------------------------------------------
FROM ${PYTHON_IMAGE} AS runtime

RUN apt-get update \
    && apt-get install --yes --no-install-recommends libimage-exiftool-perl \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system --gid 10001 picxel \
    && useradd --system --uid 10001 --gid picxel --no-create-home --shell /usr/sbin/nologin picxel

WORKDIR /srv/picxel
ENV PATH="/srv/picxel/.venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

COPY --from=builder /srv/picxel/.venv ./.venv
COPY alembic.ini ./
COPY migrations ./migrations
COPY app ./app
COPY --from=assets /srv/picxel/app/web/static/css/app.css ./app/web/static/css/app.css

ARG GIT_SHA=unknown
ARG BUILD_TIME=
ENV PICXEL_GIT_SHA=${GIT_SHA} \
    PICXEL_BUILD_TIME=${BUILD_TIME}

USER picxel
EXPOSE 8080
CMD ["picxel", "serve"]
