# Phase 2 Outlook

Phase 1 of `gdynia-thermal-db` establishes the data inventory, confirmed-source acquisition, and
district-level building metrics.  The following capabilities are explicitly deferred to Phase 2.

## Thermal Raster Download

**Goal:** Retrieve full-resolution XYZ tiles from `termalne.obliview.com` for the Gdynia bounding box.

**Approach (planned):**
1. Determine the optimal zoom level(s) from the viewer configuration.
2. Enumerate tiles using `mercantile` for the Gdynia bounding box.
3. Download tiles with rate-limiting and resume support.
4. Mosaic tiles into a single GeoTIFF per zoom level using `rasterio.merge`.
5. Store in `data/processed/raster/thermal_mosaic_{zoom}.tif`.

**Blocker:** Terms-of-use clarification for bulk tile harvesting is pending.

## Per-Building Thermal Metrics

Once the thermal mosaic is available, zonal statistics (mean, min, max, std of pixel values) will
be extracted per building footprint using `rasterstats` or `exactextract`.  Results will be added
as columns to `buildings_master.gpkg`.

## Socioeconomic Linkage

**Potential sources:**
- Central Statistical Office (GUS / BDL) – demographic and housing data at census-section level.
- Building energy certificates (CEEB) – energy performance class per address.

Linkage requires a reliable building-to-address join, which is not yet implemented.

## Machine Learning / Anomaly Detection

Planned explorations include:
- Clustering districts by thermal profile + building density.
- Identifying buildings with anomalously high thermal emission (energy loss indicators).
- Time-series change detection if multi-year thermal imagery becomes available.

## Interactive Dashboard

A lightweight Streamlit or Panel dashboard to browse district metrics and thermal maps interactively.

## Timeline

Phase 2 scope is not yet scheduled.  Community contributions are welcome – see the repository
`CONTRIBUTING` guidelines (to be added).
