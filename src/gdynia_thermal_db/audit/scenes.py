"""Parse and catalog viewer scene/config JSON files."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def parse_scene_json(path: Path | str) -> dict[str, Any]:
    """Load and lightly parse a scene JSON file.

    Args:
        path: Path to the JSON file.

    Returns:
        Parsed JSON as a dictionary, or empty dict on error.
    """
    path = Path(path)
    if not path.exists():
        logger.warning("Scene file not found: %s", path)
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        logger.info("Parsed scene JSON: %s (%d top-level keys)", path, len(data))
        return data
    except json.JSONDecodeError as exc:
        logger.error("Failed to parse JSON %s: %s", path, exc)
        return {}


def extract_layer_urls(scene: dict[str, Any]) -> list[str]:
    """Extract any URL-like strings from a scene dictionary (recursive).

    Args:
        scene: Parsed scene JSON dictionary.

    Returns:
        List of URL strings found anywhere in the scene.
    """
    urls: list[str] = []

    def _recurse(obj: Any) -> None:
        if isinstance(obj, dict):
            for v in obj.values():
                _recurse(v)
        elif isinstance(obj, list):
            for item in obj:
                _recurse(item)
        elif isinstance(obj, str) and (obj.startswith("http://") or obj.startswith("https://")):
            urls.append(obj)

    _recurse(scene)
    return list(set(urls))
