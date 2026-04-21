"""Thermal tile inventory and download helpers."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd

from gdynia_thermal_db.utils.paths import ensure_dir

logger = logging.getLogger(__name__)

# The thermal component appears to load as JPG image tiles.
# The exact tile URL pattern needs to be confirmed via network inspection.
# These are candidate/inferred patterns for inventory purposes.
CANDIDATE_TILE_PATTERNS: list[dict[str, Any]] = [
    {
        "pattern_name": "wmts_jpg_tiles",
        "url_template": "https://termalne.obliview.com/mapa/tiles/{z}/{x}/{y}.jpg",
        "status": "inferred",
        "notes": (
            "Inferred XYZ tile pattern for thermal JPGs. "
            "Needs verification by network inspection."
        ),
    },
    {
        "pattern_name": "wmts_jpg_tiles_alt",
        "url_template": "https://termalne.obliview.com/tiles/{z}/{x}/{y}.jpg",
        "status": "inferred",
        "notes": "Alternate tile path pattern. Needs verification.",
    },
]


def build_tile_inventory(
    tile_patterns: list[dict[str, Any]] | None = None,
) -> pd.DataFrame:
    """Build a thermal tile inventory DataFrame from known patterns.

    This function records candidate tile URL patterns for inventory purposes.
    Actual tile availability must be verified separately.

    Args:
        tile_patterns: List of pattern dicts. Defaults to
            :data:`CANDIDATE_TILE_PATTERNS`.

    Returns:
        DataFrame with one row per known or inferred tile pattern.
    """
    if tile_patterns is None:
        tile_patterns = CANDIDATE_TILE_PATTERNS

    rows = []
    for pattern in tile_patterns:
        rows.append(
            {
                "pattern_name": pattern.get("pattern_name"),
                "url_template": pattern.get("url_template"),
                "status": pattern.get("status", "unknown"),
                "notes": pattern.get("notes", ""),
            }
        )

    df = pd.DataFrame(rows)
    logger.info("Built tile inventory with %d patterns", len(df))
    return df


def normalize_tile_name(z: int, x: int, y: int, ext: str = "jpg") -> str:
    """Generate a normalized filename for a tile.

    Args:
        z: Zoom level.
        x: Tile column.
        y: Tile row.
        ext: File extension (without dot).

    Returns:
        Normalized tile filename string.
    """
    return f"tile_{z}_{x}_{y}.{ext}"


def save_tile_inventory(df: pd.DataFrame, output_path: Path | str) -> Path:
    """Save the tile inventory DataFrame to CSV.

    Args:
        df: Tile inventory DataFrame.
        output_path: Destination CSV path.

    Returns:
        Resolved output path.
    """
    output_path = Path(output_path)
    ensure_dir(output_path.parent)
    df.to_csv(output_path, index=False)
    logger.info("Tile inventory saved to %s", output_path)
    return output_path
