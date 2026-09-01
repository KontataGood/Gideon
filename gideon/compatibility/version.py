"""
Gideon compatibility and version information.
"""

GIDEON_VERSION = "0.1.0"
GIDEON_API_VERSION = 1


def get_version() -> str:
    """Возвращает текущую версию Gideon."""

    return GIDEON_VERSION


def get_api_version() -> int:
    """Возвращает версию внутреннего API Gideon."""

    return GIDEON_API_VERSION