# Limitations

## Thermal Data Availability

The thermal imagery hosted at `termalne.obliview.com` is publicly viewable but **not distributed as
a bulk download**.  The raster tiles can be individually requested via standard XYZ tile URLs, but:

- Full-resolution coverage requires thousands of tile requests.
- The terms of use for bulk tile harvesting are not explicitly stated.
- As a result, this project treats thermal rasters as **inventory-first**: tile URLs are catalogued
  but not bulk-downloaded in Phase 1.

Practical consequence: the current dataset cannot produce per-building thermal statistics until
Phase 2 implements a responsible tile acquisition strategy.

## Buildings Layer Coverage

`budynki.geojson` contains the building footprints published by the thermal viewer.  This layer:

- May not reflect the most recent cadastral data.
- Does not include building attributes such as year of construction, number of floors, or energy
  performance class.
- Geometry quality has not been independently validated against official cadastral sources.

## District Boundaries

- District boundaries are taken from Gdynia Open Data; the dataset version and date of last update
  are not embedded in the download and should be verified manually.
- Minor boundary adjustments may occur between dataset releases.

## No Socioeconomic Data

The current implementation does not incorporate socioeconomic or demographic data.
Such linkages are deferred to Phase 2.

## Coordinate Precision

GeoJSON inputs use WGS 84 with six decimal places (~0.1 m precision), which is sufficient for
district-level aggregation but may introduce sub-metre offsets when overlaid against precise
cadastral data in EPSG:2180.

## Network Dependency

Source acquisition requires internet access.  The pipeline will fail gracefully if a source URL
is unreachable, recording the error in the source inventory rather than raising an exception.

## Scope

This project is a **research prototype**, not a production system.  It is not affiliated with the
City of Gdynia or Obliview.
