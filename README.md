# Picxel

**See what's really in your pixels.**

Picxel is an open-source web app that inspects any image for signs of AI generation and provenance, and shows you the evidence. Then it exports a pixel-perfect version for every platform, with its disclosure intact.

> **Status: Phase 0 (Foundations).** Not usable yet. Progress lives in [`agent.md`](agent.md).

## Why Picxel
- **Evidence, not a mystery percentage.** Content Credentials (C2PA), metadata, watermarks, and a calibrated detector, each explained.
- **Privacy-first.** Images are processed in memory and never stored.
- **Honest by design.** Published accuracy numbers, and we never strip AI disclosures ([why](decision.md#d-001--pivot-no-detector-evasion--inspector--studio)).

## Quick start
You need [uv](https://docs.astral.sh/uv/getting-started/installation/). It installs Python 3.12 for you.

```bash
uv sync                  # create .venv with everything
uv run pre-commit install
uv run picxel dev        # http://127.0.0.1:8000, auto-reload + live CSS
```

With Docker (app + PostgreSQL + migrations):

```bash
docker compose up --build   # http://localhost:8000
```

## Commands

| Command | What it does |
|---|---|
| `uv run picxel dev` | Dev server with auto-reload and Tailwind watch |
| `uv run picxel check` | Lint, format check, types, import contracts, tests + coverage |
| `uv run picxel css` | Build the minified stylesheet |
| `uv run picxel migrate` | Apply database migrations |
| `uv run picxel serve` | Production server (the container's entry point) |

## Stack
Python 3.12 · FastAPI · Jinja2 · Tailwind CSS (standalone, no Node) · SQLAlchemy 2 + Alembic · PostgreSQL (Neon) · Google Cloud Run · Cloudflare

## Project documents

| File | Purpose |
|---|---|
| [`project.md`](project.md) | The plan: vision, architecture, roadmap, quality bar |
| [`agent.md`](agent.md) | Current state: what's done, what's next, open questions |
| [`decision.md`](decision.md) | Every deviation from the plan, with reasoning |

## Contributing
Start with [CONTRIBUTING.md](CONTRIBUTING.md). Please read the [Code of Conduct](CODE_OF_CONDUCT.md). Report vulnerabilities privately, following [SECURITY.md](SECURITY.md).

## License
Code: [AGPL-3.0-or-later](LICENSE). Documentation and content: CC BY 4.0.
