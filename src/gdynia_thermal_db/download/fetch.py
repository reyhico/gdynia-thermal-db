"""Generic HTTP fetch utilities with retry and provenance tracking."""

from __future__ import annotations

import datetime
import logging
import time
from pathlib import Path
from typing import Any

import requests

from gdynia_thermal_db.utils.hashing import sha256_file
from gdynia_thermal_db.utils.paths import ensure_dir

logger = logging.getLogger(__name__)


def fetch_file(
    url: str,
    dest: Path | str,
    timeout: int = 30,
    retries: int = 3,
    backoff: float = 2.0,
    user_agent: str = "gdynia-thermal-db/1.0",
    overwrite: bool = False,
    stream: bool = True,
) -> dict[str, Any]:
    """Download a file from a URL with retry logic.

    Args:
        url: Source URL.
        dest: Local destination file path.
        timeout: Request timeout in seconds.
        retries: Number of retry attempts on failure.
        backoff: Exponential backoff base in seconds.
        user_agent: HTTP User-Agent string.
        overwrite: If False, skip if file already exists.
        stream: Stream the response (recommended for large files).

    Returns:
        Dictionary with download metadata including checksum.
    """
    dest = Path(dest)
    ensure_dir(dest.parent)

    result: dict[str, Any] = {
        "url": url,
        "local_path": str(dest),
        "retrieval_timestamp": datetime.datetime.utcnow().isoformat(),
        "status_code": None,
        "content_type": None,
        "file_size_bytes": None,
        "checksum_sha256": None,
        "skipped": False,
        "error": None,
    }

    if dest.exists() and not overwrite:
        logger.info("Already exists, skipping: %s", dest)
        result["skipped"] = True
        result["file_size_bytes"] = dest.stat().st_size
        result["checksum_sha256"] = sha256_file(dest)
        return result

    headers = {"User-Agent": user_agent}
    last_exc: Exception | None = None

    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=timeout, stream=stream)
            result["status_code"] = resp.status_code
            result["content_type"] = resp.headers.get("Content-Type")

            if not resp.ok:
                result["error"] = f"HTTP {resp.status_code}"
                logger.warning(
                    "Attempt %d/%d: HTTP %d for %s",
                    attempt, retries, resp.status_code, url,
                )
                break

            with open(dest, "wb") as f:
                for chunk in resp.iter_content(chunk_size=65536):
                    f.write(chunk)

            result["file_size_bytes"] = dest.stat().st_size
            result["checksum_sha256"] = sha256_file(dest)
            logger.info(
                "Downloaded %s → %s (%d bytes)",
                url, dest, result["file_size_bytes"],
            )
            return result

        except requests.RequestException as exc:
            last_exc = exc
            logger.warning(
                "Attempt %d/%d failed for %s: %s", attempt, retries, url, exc
            )
            if attempt < retries:
                wait = backoff ** attempt
                logger.info("Retrying in %.1f seconds...", wait)
                time.sleep(wait)

    if last_exc is not None:
        result["error"] = str(last_exc)

    return result
