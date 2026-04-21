"""File hashing utilities for provenance tracking."""

from __future__ import annotations

import hashlib
from pathlib import Path


BLOCK_SIZE = 65536


def sha256_file(path: Path | str) -> str:
    """Compute the SHA-256 checksum of a file.

    Args:
        path: Path to the file.

    Returns:
        Lowercase hex-encoded SHA-256 digest.
    """
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(BLOCK_SIZE):
            h.update(chunk)
    return h.hexdigest()


def md5_file(path: Path | str) -> str:
    """Compute the MD5 checksum of a file.

    Args:
        path: Path to the file.

    Returns:
        Lowercase hex-encoded MD5 digest.
    """
    h = hashlib.md5()
    with open(path, "rb") as f:
        while chunk := f.read(BLOCK_SIZE):
            h.update(chunk)
    return h.hexdigest()
