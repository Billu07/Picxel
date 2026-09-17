"""The ``picxel`` command: developer workflows and the container entry point.

Only the standard library is imported at module level, so ``python -m app.cli css`` also works in
the Docker assets stage, where application dependencies aren't installed.
"""

import argparse
import os
import shutil
import subprocess
import sys
from collections.abc import Callable, Sequence
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSS_DIR = PROJECT_ROOT / "app" / "web" / "static" / "css"

# Single pin for the Tailwind standalone CLI, which pytailwindcss downloads on first use.
TAILWIND_VERSION = "v4.3.3"

CHECKS: tuple[tuple[str, list[str]], ...] = (
    ("ruff lint", ["ruff", "check", "."]),
    ("ruff format", ["ruff", "format", "--check", "."]),
    ("mypy", ["mypy"]),
    ("import contracts", ["lint-imports"]),
    ("tests", ["pytest", "--cov"]),
)


def _run(command: Sequence[str]) -> int:
    print(f"$ {' '.join(command)}", flush=True)
    return subprocess.call(list(command), cwd=PROJECT_ROOT)


def _tailwind_command(*, watch: bool, minify: bool) -> list[str]:
    executable = shutil.which("tailwindcss")
    if executable is None:
        sys.exit("tailwindcss not found. Install the assets group: uv sync --group assets")
    os.environ.setdefault("TAILWINDCSS_VERSION", TAILWIND_VERSION)
    command = [
        executable,
        "--input",
        str(CSS_DIR / "input.css"),
        "--output",
        str(CSS_DIR / "app.css"),
    ]
    if watch:
        command.append("--watch=always")
    if minify:
        command.append("--minify")
    return command


def css(*, watch: bool) -> int:
    return _run(_tailwind_command(watch=watch, minify=not watch))


def dev(host: str, port: int) -> int:
    import uvicorn

    from app.core.logging import configure_logging

    configure_logging("INFO", json_output=False)
    css_watcher = subprocess.Popen(_tailwind_command(watch=True, minify=False), cwd=PROJECT_ROOT)
    try:
        uvicorn.run(
            "app.main:app",
            host=host,
            port=port,
            reload=True,
            reload_dirs=[str(PROJECT_ROOT / "app")],
            log_config=None,
        )
    finally:
        css_watcher.terminate()
    return 0


def serve() -> int:
    import uvicorn

    from app.core.config import get_settings
    from app.core.logging import configure_logging

    settings = get_settings()
    configure_logging(settings.log_level, json_output=settings.is_deployed)
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",  # noqa: S104 - containers must listen on all interfaces
        port=int(os.environ.get("PORT", "8080")),
        proxy_headers=True,
        forwarded_allow_ips="*",  # only Cloud Run's front end can reach the container
        log_config=None,
        server_header=False,
    )
    return 0


def migrate() -> int:
    from app.core.config import get_settings
    from app.core.logging import configure_logging
    from app.db.migrations import upgrade_to_head

    settings = get_settings()
    configure_logging(settings.log_level, json_output=settings.is_deployed)
    database_url = settings.sqlalchemy_database_url
    if database_url is None:
        print("PICXEL_DATABASE_URL is not set; nothing to migrate.", file=sys.stderr)
        return 2
    upgrade_to_head(database_url)
    return 0


def check() -> int:
    failed = [name for name, command in CHECKS if _run(command) != 0]
    if failed:
        print(f"\nFailed: {', '.join(failed)}", file=sys.stderr)
        return 1
    print("\nAll checks passed.")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="picxel", description="Picxel developer and runtime commands."
    )
    commands = parser.add_subparsers(dest="command", required=True, metavar="COMMAND")

    dev_parser = commands.add_parser(
        "dev", help="run the app with auto-reload and live CSS rebuilds"
    )
    dev_parser.add_argument("--host", default="127.0.0.1")
    dev_parser.add_argument("--port", type=int, default=8000)
    commands.add_parser("serve", help="run the production server (container entry point)")
    css_parser = commands.add_parser("css", help="build the Tailwind stylesheet")
    css_parser.add_argument("--watch", action="store_true", help="rebuild when templates change")
    commands.add_parser("migrate", help="apply database migrations")
    commands.add_parser("check", help="run lint, format, types, import contracts, and tests")

    args = parser.parse_args(argv)
    handlers: dict[str, Callable[[], int]] = {
        "dev": lambda: dev(args.host, args.port),
        "serve": serve,
        "css": lambda: css(watch=args.watch),
        "migrate": migrate,
        "check": check,
    }
    return handlers[args.command]()


if __name__ == "__main__":
    sys.exit(main())
