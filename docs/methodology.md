# Methodology

## Overview

The `gdynia-thermal-db` project collects, processes, and analyses geospatial data related to the
publicly available Gdynia thermal map.  The workflow proceeds in four stages:

1. **Source audit** – enumerate confirmed URLs and assets from the thermal viewer.
2. **Data acquisition** – download confirmed public layers (buildings, district boundaries).
3. **Database build** – clean, reproject, and join layers into a unified GeoPackage/Parquet store.
4. **Indicator computation** – aggregate building-level attributes to district summaries.

## Coordinate Reference Systems

| Stage | CRS | Rationale |
|-------|-----|-----------|
| Raw download | EPSG:4326 (WGS 84) | GeoJSON default |
| Analysis | EPSG:2180 (Poland CS92) | Metric, minimises area distortion |
| Outputs | EPSG:4326 | Interoperability with web maps |

All reprojection is performed via `pyproj` / `geopandas.to_crs()`.

## Thermal Raster Treatment

Thermal raster tiles hosted at `termalne.obliview.com` are treated as **inventory-first**.
The current scope records tile metadata (zoom levels, bounding boxes, confirmed asset URLs) without
performing a full tile download.  A complete download pipeline is deferred to Phase 2.

## Quality Flags

Each processed record carries a `source_confirmed` boolean flag that reflects whether the upstream
URL was verified reachable at processing time.  Layers with `confirmed: false` in `config/config.yaml`
are included in the inventory but excluded from spatial joins.

## Reproducibility

All paths are resolved relative to the project root via `Settings` (see `src/gdynia_thermal_db/settings.py`).
Raw downloads are kept unmodified under `data/raw/` and `data/external/`.  Processed outputs are
written to `data/processed/` and `outputs/`.
