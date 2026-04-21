"""Audit and download viewer configuration assets."""

from __future__ import annotations

import logging
from pathlib import Path

import requests

from gdynia_thermal_db.utils.hashing import sha256_file
from gdynia_thermal_db.utils.paths import ensure_dir

logger = logging.getLogger(__name__)


def download_asset(
    url: str,
    dest: Path,
    timeout: int = 30,
    user_agent: str = "gdynia-thermal-db/1.0",
    overwrite: bool = False,
) -> dict:
    """Download a single viewer asset to a local path.

    Args:
        url: Source URL.
        dest: Local destination path.
        timeout: Request timeout.
        user_agent: HTTP User-Agent string.
        overwrite: If False, skip download if file already exists.

    Returns:
        Dictionary with download result metadata.
    """
    dest = Path(dest)
    ensure_dir(dest.parent)

    result = {
        "url": url,
        "local_path": str(dest),
        "skipped": False,
        "status_code": None,
        "checksum": None,
        "error": None,
    }

    if dest.exists() and not overwrite:
        logger.info("Already exists, skipping: %s", dest)
        result["skipped"] = True
        result["checksum"] = sha256_file(dest)
        return result

    headers = {"User-Agent": user_agent}
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        result["status_code"] = resp.status_code
        if resp.ok:
            dest.write_bytes(resp.content)
            result["checksum"] = sha256_file(dest)
            logger.info("Downloaded %s → %s (HTTP %d)", url, dest, resp.status_code)
        else:
            result["error"] = f"HTTP {resp.status_code}"
            logger.warning("Failed to download %s: HTTP %d", url, resp.status_code)
    except requests.RequestException as exc:
        result["error"] = str(exc)
        logger.error("Error downloading %s: %s", url, exc)

    return result
