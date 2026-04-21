"""Viewer inventory: audit and catalog public resources from the Gdynia thermal viewer."""

from __future__ import annotations

import datetime
import logging
from pathlib import Path
from typing import Any

import pandas as pd
import requests

from gdynia_thermal_db.utils.paths import ensure_dir

logger = logging.getLogger(__name__)

# Known and candidate public resources to probe
VIEWER_ASSETS: list[dict[str, Any]] = [
    {
        "source_name": "buildings_geojson",
        "source_url": "https://termalne.obliview.com/mapa/Data/Wektory/budynki.geojson",
        "source_type": "vector/geojson",
        "notes": "Confirmed public building layer",
    },
    {
        "source_name": "viewer_entry",
        "source_url": "https://termalne.obliview.com/mapa/",
        "source_type": "html/viewer",
        "notes": "Confirmed public viewer entry point",
    },
    {
        "source_name": "conf_js",
        "source_url": "https://termalne.obliview.com/mapa/conf.js",
        "source_type": "config/js",
        "notes": "Candidate viewer config",
    },
    {
        "source_name": "settings_js",
        "source_url": "https://termalne.obliview.com/mapa/settings.js",
        "source_type": "config/js",
        "notes": "Candidate viewer settings",
    },
    {
        "source_name": "gdynia_json",
        "source_url": "https://termalne.obliview.com/mapa/Data/Gdynia.json",
        "source_type": "metadata/json",
        "notes": "Candidate scene/city JSON",
    },
    {
        "source_name": "gdynia_json_alt",
        "source_url": "https://termalne.obliview.com/mapa/data/Gdynia.json",
        "source_type": "metadata/json",
        "notes": "Candidate scene/city JSON (alternate case)",
    },
    {
        "source_name": "districts_zip",
        "source_url": (
            "https://otwartedane.gdynia.pl/pl/dataset/"
            "6197975f-bfb2-4ccd-a56f-6dd645048a88/resource/"
            "973c73dc-82cd-4da6-a771-f4b7826036e1/download/dzielnice_gdyni.zip"
        ),
        "source_type": "vector/shapefile-zip",
        "notes": "Official Gdynia district boundaries (Mapa Gdyni open data)",
    },
]


def probe_url(
    url: str,
    timeout: int = 30,
    user_agent: str = "gdynia-thermal-db/1.0",
) -> dict[str, Any]:
    """Probe a single URL and return status metadata.

    Args:
        url: URL to probe.
        timeout: Request timeout in seconds.
        user_agent: HTTP User-Agent header.

    Returns:
        Dictionary with probe results.
    """
    headers = {"User-Agent": user_agent}
    result: dict[str, Any] = {
        "source_url": url,
        "retrieval_timestamp": datetime.datetime.utcnow().isoformat(),
        "status_code": None,
        "content_type": None,
        "content_length": None,
        "error": None,
    }
    try:
        resp = requests.head(url, headers=headers, timeout=timeout, allow_redirects=True)
        result["status_code"] = resp.status_code
        result["content_type"] = resp.headers.get("Content-Type")
        result["content_length"] = resp.headers.get("Content-Length")
    except requests.RequestException as exc:
        result["error"] = str(exc)
        logger.warning("Failed to probe %s: %s", url, exc)
    return result


def build_inventory(
    assets: list[dict[str, Any]] | None = None,
    timeout: int = 30,
) -> pd.DataFrame:
    """Build a source inventory table by probing all known assets.

    Args:
        assets: List of asset dicts to probe. Defaults to :data:`VIEWER_ASSETS`.
        timeout: HTTP request timeout in seconds.

    Returns:
        DataFrame with one row per asset.
    """
    if assets is None:
        assets = VIEWER_ASSETS

    rows = []
    for asset in assets:
        logger.info("Probing: %s", asset["source_url"])
        probe = probe_url(asset["source_url"], timeout=timeout)
        row = {**asset, **probe}
        rows.append(row)
        logger.info(
            "  %s → %s",
            asset["source_name"],
            probe.get("status_code", "ERROR"),
        )

    df = pd.DataFrame(rows)
    # Reorder columns
    cols = [
        "source_name",
        "source_url",
        "source_type",
        "status_code",
        "content_type",
        "content_length",
        "retrieval_timestamp",
        "error",
        "notes",
    ]
    existing_cols = [c for c in cols if c in df.columns]
    df = df[existing_cols]
    return df


def save_inventory(df: pd.DataFrame, output_path: Path | str) -> Path:
    """Save the inventory DataFrame to CSV.

    Args:
        df: Inventory DataFrame.
        output_path: Destination CSV path.

    Returns:
        Resolved output path.
    """
    output_path = Path(output_path)
    ensure_dir(output_path.parent)
    df.to_csv(output_path, index=False)
    logger.info("Inventory saved to %s (%d rows)", output_path, len(df))
    return output_path
