# gdynia-thermal-db

Research-grade geospatial data engineering for the Gdynia thermal map project.

Data is sourced from the public thermal viewer at
[termalne.obliview.com/mapa/](https://termalne.obliview.com/mapa/) and the
[Gdynia Open Data Portal](https://otwartedane.gdynia.pl/).

---

## Documentation

| Document | Description |
|----------|-------------|
| [docs/methodology.md](docs/methodology.md) | Workflow stages, CRS choices, and reproducibility notes |
| [docs/data_sources.md](docs/data_sources.md) | Confirmed and provisional data sources |
| [docs/database_design.md](docs/database_design.md) | Directory layout and layer schemas |
| [docs/admin_units.md](docs/admin_units.md) | Gdynia district boundaries source and processing |
| [docs/limitations.md](docs/limitations.md) | Known constraints and out-of-scope items |
| [docs/phase2_outlook.md](docs/phase2_outlook.md) | Planned Phase 2 capabilities |

## Notebooks

Run notebooks in order; each prerequisite is noted in the first cell.

| Notebook | Description |
|----------|-------------|
| [01_viewer_audit.ipynb](notebooks/01_viewer_audit.ipynb) | Enumerate and probe data sources; produce `source_inventory.csv` |
| [02_download_buildings.ipynb](notebooks/02_download_buildings.ipynb) | Download `budynki.geojson` and save raw GeoPackage |
| [03_admin_units.ipynb](notebooks/03_admin_units.ipynb) | Download and process district boundaries |
| [04_thermal_tiles_inventory.ipynb](notebooks/04_thermal_tiles_inventory.ipynb) | Catalogue thermal tile URLs (inventory only, no bulk download) |
| [05_database_build.ipynb](notebooks/05_database_build.ipynb) | Join buildings + districts into master table |
| [06_district_metrics.ipynb](notebooks/06_district_metrics.ipynb) | Compute per-district building summaries |

## Quick Start

```bash
# Install in development mode
pip install -e ".[dev]"

# Copy and edit environment variables
cp .env.example .env

# Run notebooks in order with Jupyter
jupyter notebook notebooks/
```

## Project Structure

```
config/          – YAML configuration (sources, paths, CRS)
docs/            – Project documentation
notebooks/       – Analysis notebooks (run in numbered order)
src/             – Python package (gdynia_thermal_db)
tests/           – Unit tests
outputs/         – Generated tables and maps (git-ignored)
data/            – Downloaded and processed data (git-ignored)
```

## Licence

MIT – see [LICENSE](LICENSE).