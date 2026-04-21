"""Download viewer configuration and metadata assets."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from gdynia_thermal_db.download.fetch import fetch_file

logger = logging.getLogger(__name__)

VIEWER_ASSET_LIST: list[dict[str, Any]] = [
    {
        "name": "conf_js",
        "url": "https://termalne.obliview.com/mapa/conf.js",
        "dest": "data/raw/viewer/conf.js",
    },
    {
        "name": "settings_js",
        "url": "https://termalne.obliview.com/mapa/settings.js",
        "dest": "data/raw/viewer/settings.js",
    },
    {
        "name": "gdynia_json",
        "url": "https://termalne.obliview.com/mapa/Data/Gdynia.json",
        "dest": "data/raw/metadata/Gdynia.json",
    },
    {
        "name": "viewer_index",
        "url": "https://termalne.obliview.com/mapa/",
        "dest": "data/raw/viewer/index.html",
    },
]


def download_viewer_assets(
    asset_list: list[dict[str, Any]] | None = None,
    overwrite: bool = False,
    timeout: int = 30,
) -> list[dict[str, Any]]:
    """Download all known viewer configuration assets.

    Args:
        asset_list: List of asset dicts with ``name``, ``url``, ``dest`` keys.
        overwrite: Overwrite existing files if True.
        timeout: HTTP timeout in seconds.

    Returns:
        List of download result dictionaries.
    """
    if asset_list is None:
        asset_list = VIEWER_ASSET_LIST

    results = []
    for asset in asset_list:
        logger.info("Fetching viewer asset: %s → %s", asset["name"], asset["url"])
        result = fetch_file(
            url=asset["url"],
            dest=Path(asset["dest"]),
            timeout=timeout,
            overwrite=overwrite,
        )
        result["asset_name"] = asset["name"]
        results.append(result)
    return results
