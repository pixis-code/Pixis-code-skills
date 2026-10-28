"""Resolve PIXIS_HOME. Uses pixis_constants when importable, else env."""

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
