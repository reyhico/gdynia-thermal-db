"""URL utility helpers."""

from __future__ import annotations

import re
from urllib.parse import urljoin, urlparse


def normalize_url(url: str) -> str:
    """Normalize a URL by stripping trailing slashes and whitespace.

    Args:
        url: Input URL string.

    Returns:
        Normalized URL string.
    """
    return url.strip().rstrip("/")


def safe_filename(url: str) -> str:
    """Derive a safe local filename from a URL.

    Args:
        url: Source URL.

    Returns:
        A filesystem-safe filename string.
    """
    parsed = urlparse(url)
    name = parsed.path.split("/")[-1] or "index"
    # Replace any characters that are not alphanumeric, dot, dash, or underscore
    name = re.sub(r"[^\w.\-]", "_", name)
    return name


def join_url(base: str, *parts: str) -> str:
    """Join URL parts together.

    Args:
        base: Base URL.
        *parts: Additional path segments.

    Returns:
        Combined URL string.
    """
    result = base
    for part in parts:
        result = urljoin(result.rstrip("/") + "/", part.lstrip("/"))
    return result
