"""Static project metadata."""

from functools import cache
from importlib.metadata import PackageNotFoundError, version

PROJECT_NAME = "picxel"
REPOSITORY_URL = "https://github.com/Billu07/Picxel"


@cache
def package_version() -> str:
    try:
        return version(PROJECT_NAME)
    except PackageNotFoundError:  # running from a source tree that was never installed
        return "0.0.0+unknown"
