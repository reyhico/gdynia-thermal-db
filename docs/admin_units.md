# Administrative Units

## Source

District boundaries for Gdynia are sourced from the **Gdynia Open Data Portal** (*otwartedane.gdynia.pl*),
specifically the *Mapa Gdyni* dataset:

- **File:** `Dzielnice_Gdyni.zip`
- **Format:** ESRI Shapefile (zipped)
- **Native CRS:** EPSG:2180 (Poland CS92)
- **Licence:** Open government data (Creative Commons / public domain equivalent)

The dataset contains the 22 official administrative districts (*dzielnice*) of Gdynia.

## Processing Steps

1. Download `Dzielnice_Gdyni.zip` to `data/external/admin_units/`.
2. Extract and read the shapefile with `geopandas.read_file()`.
3. Standardise column names to `district_id` and `district_name`.
4. Verify CRS is EPSG:2180; reproject if necessary.
5. Validate geometries with `make_valid()`.
6. Write to `data/processed/admin_units/gdynia_districts.gpkg`.

## District Identifiers

District identifiers are derived from the shapefile's native attribute field.  The exact field name
may vary between dataset versions; the processing script resolves this dynamically.

## Usage in the Pipeline

District boundaries are used for:
- Spatial join with the buildings layer (point-in-polygon or overlay).
- Aggregation of building-level metrics to district summaries.
- Choropleth map generation in `outputs/maps/`.

## Notes

- The district layer is relatively stable; re-download is only required if the Open Data Portal
  releases an updated version.
- Municipal boundary of Gdynia itself is the union of all 22 districts.
- Notebook `03_admin_units.ipynb` contains exploratory analysis of this layer.
