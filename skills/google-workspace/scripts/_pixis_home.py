"""Resolve PIXIS_HOME for standalone skill scripts.

Skill scripts may run outside the Pixis process where ``pixis_constants``
is not importable. Prefer ``pixis_constants`` when available; otherwise
fall back to ``PIXIS_HOME`` or ``~/.pixis``.
"""

from __future__ import annotations

import os
from pathlib import Path

try:
    from pixis_constants import get_pixis_home
except (ModuleNotFoundError, ImportError):

    def get_pixis_home() -> Path:
        """Return the Pixis home directory (default: ``~/.pixis``)."""
        val = os.environ.get("PIXIS_HOME", "").strip()
        return Path(val) if val else Path.home() / ".pixis"


def display_pixis_home() -> str:
    """Return a user-friendly ``~/``-shortened display string."""
    home = get_pixis_home()
    try:
        return "~/" + home.relative_to(Path.home()).as_posix()
    except ValueError:
        return str(home)
