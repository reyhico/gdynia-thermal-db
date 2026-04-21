# Database Design

## Overview

The project uses a **mixed raster + vector** storage model.  Vector data is managed in GeoPackage
(`.gpkg`) files and exported to Parquet for downstream analysis; raster inventory metadata is stored
in CSV until a full tile download is implemented.

## Directory Layout

```
data/
├── raw/
│   ├── vector/         # Downloaded GeoJSON files (buildings)
│   └── viewer/         # Cached viewer config assets
├── external/
│   └── admin_units/    # Dzielnice_Gdyni.zip (official boundaries)
├── interim/            # Intermediate working files
└── processed/
    ├── buildings/      # Cleaned + enriched building layers
    └── admin_units/    # Reprojected district boundaries

outputs/
├── tables/             # CSV indicator tables
├── maps/               # Static map exports
└── logs/               # Run logs
```

## Vector Layers

### `buildings_raw.gpkg`
Raw building footprints from `budynki.geojson`, reprojected to EPSG:2180.

### `buildings_clean.gpkg`
Geometrically valid buildings: invalid geometries fixed with `make_valid()`, duplicates removed.

### `buildings_master.gpkg` / `buildings_master.parquet`
Master building table with district join, computed area (`area_m2`), and source flags.

| Column | Type | Description |
|--------|------|-------------|
| `geometry` | Polygon | Building footprint (EPSG:2180) |
| `area_m2` | float | Computed area in square metres |
| `district_id` | str | Joined district identifier |
| `district_name` | str | Human-readable district name |
| `source_confirmed` | bool | Whether source URL was reachable |

### `gdynia_districts.gpkg`
Official district boundaries reprojected to EPSG:2180.

| Column | Type | Description |
|--------|------|-------------|
| `geometry` | Polygon/MultiPolygon | District boundary |
| `district_id` | str | Unique district code |
| `district_name` | str | District name (Polish) |

## Raster Inventory

Thermal raster tiles are catalogued in `outputs/tables/thermal_tiles_inventory.csv`.  Each row
represents one discovered tile URL with columns:

| Column | Description |
|--------|-------------|
| `url` | Full tile URL |
| `zoom` | Tile zoom level |
| `x`, `y` | Tile coordinates |
| `confirmed` | Whether HTTP HEAD returned 200 |

Full tile download is deferred to Phase 2.

## Source Inventory

`outputs/tables/source_inventory.csv` lists all configured data sources with their confirmation
status, local paths, and last-checked timestamps.
