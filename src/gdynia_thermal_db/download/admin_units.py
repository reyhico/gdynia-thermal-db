"""Download and prepare administrative unit data."""

from __future__ import annotations

import logging
import zipfile
from pathlib import Path

from gdynia_thermal_db.download.fetch import fetch_file
from gdynia_thermal_db.utils.paths import ensure_dir

logger = logging.getLogger(__name__)

DISTRICTS_URL = (
    "https://otwartedane.gdynia.pl/pl/dataset/"
    "6197975f-bfb2-4ccd-a56f-6dd645048a88/resource/"
    "973c73dc-82cd-4da6-a771-f4b7826036e1/download/dzielnice_gdyni.zip"
)
DEFAULT_DEST = Path("data/external/admin_units/Dzielnice_Gdyni.zip")


def download_districts(
    dest: Path | str = DEFAULT_DEST,
    overwrite: bool = False,
    timeout: int = 60,
) -> dict:
    """Download the Gdynia district boundaries ZIP from the open data portal.

    The preferred district source is the official Gdynia open data dataset
    "Mapa Gdyni" (Dzielnice_Gdyni.zip).

    Args:
        dest: Local destination path.
        overwrite: Overwrite if True.
        timeout: HTTP timeout in seconds.

    Returns:
        Download result metadata dictionary.
    """
    logger.info("Downloading Gdynia district boundaries from %s", DISTRICTS_URL)
    result = fetch_file(
        url=DISTRICTS_URL,
        dest=Path(dest),
        timeout=timeout,
        overwrite=overwrite,
    )
    if result.get("error"):
        logger.error("Districts download failed: %s", result["error"])
    else:
        logger.info("Districts saved to %s", result["local_path"])
    return result


def extract_districts_zip(
    zip_path: Path | str = DEFAULT_DEST,
    extract_dir: Path | str | None = None,
) -> Path:
    """Extract the district boundaries ZIP file.

    Args:
        zip_path: Path to the downloaded ZIP file.
        extract_dir: Directory to extract into. Defaults to the same
            directory as the ZIP file.

    Returns:
        Path to the extraction directory.
    """
    zip_path = Path(zip_path)
    if extract_dir is None:
        extract_dir = zip_path.parent / zip_path.stem
    extract_dir = Path(extract_dir)
    ensure_dir(extract_dir)

    if not zip_path.exists():
        raise FileNotFoundError(f"ZIP not found: {zip_path}")

    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_dir)
        extracted = zf.namelist()

    logger.info(
        "Extracted %d files from %s -> %s", len(extracted), zip_path, extract_dir
    )
    return extract_dir
