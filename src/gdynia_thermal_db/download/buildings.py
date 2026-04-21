"""Download the public building GeoJSON from the Gdynia thermal viewer."""

from __future__ import annotations

import logging
from pathlib import Path

from gdynia_thermal_db.download.fetch import fetch_file

logger = logging.getLogger(__name__)

BUILDINGS_URL = "https://termalne.obliview.com/mapa/Data/Wektory/budynki.geojson"
DEFAULT_DEST = Path("data/raw/vector/budynki.geojson")


def download_buildings(
    dest: Path | str = DEFAULT_DEST,
    overwrite: bool = False,
    timeout: int = 60,
) -> dict:
    """Download the Gdynia building GeoJSON.

    Args:
        dest: Local destination path.
        overwrite: Overwrite existing file if True.
        timeout: HTTP timeout in seconds.

    Returns:
        Download result metadata dictionary.
    """
    logger.info("Downloading building layer from %s", BUILDINGS_URL)
    result = fetch_file(
        url=BUILDINGS_URL,
        dest=Path(dest),
        timeout=timeout,
        overwrite=overwrite,
    )
    if result.get("error"):
        logger.error("Building download failed: %s", result["error"])
    else:
        logger.info("Buildings saved to %s", result["local_path"])
    return result
