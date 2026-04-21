# Data Sources

## Confirmed Sources

### 1. Public Buildings Layer

| Field | Value |
|-------|-------|
| URL | `https://termalne.obliview.com/mapa/Data/Wektory/budynki.geojson` |
| Format | GeoJSON (EPSG:4326) |
| Confirmed | ✅ Yes |
| Local path | `data/raw/vector/budynki.geojson` |
| Notes | Public building footprints served by the Gdynia thermal viewer |

### 2. Gdynia District Boundaries

| Field | Value |
|-------|-------|
| Source | Gdynia Open Data Portal |
| Dataset | *Mapa Gdyni* – Dzielnice |
| URL | `https://otwartedane.gdynia.pl/pl/dataset/6197975f-bfb2-4ccd-a56f-6dd645048a88/...` |
| File | `Dzielnice_Gdyni.zip` (shapefile inside ZIP) |
| Format | ESRI Shapefile (EPSG:2180) |
| Confirmed | ✅ Yes |
| Local path | `data/external/admin_units/Dzielnice_Gdyni.zip` |

### 3. Gdynia Thermal Viewer

| Field | Value |
|-------|-------|
| Base URL | `https://termalne.obliview.com/mapa/` |
| Confirmed | ✅ Yes |
| Notes | Public GIS viewer entry point; hosts raster tiles and vector overlays |

## Unconfirmed / Provisional Sources

The following viewer assets are listed in `config/config.yaml` with `confirmed: false`.
They are included in the source inventory but not fetched by default.

| Name | URL |
|------|-----|
| `conf.js` | `https://termalne.obliview.com/mapa/conf.js` |
| `settings.js` | `https://termalne.obliview.com/mapa/settings.js` |
| `Gdynia.json` | `https://termalne.obliview.com/mapa/Data/Gdynia.json` |

## Out-of-Scope Sources (Phase 2)

- Individual thermal raster tiles (full mosaic download)
- Socioeconomic datasets (GUS, BDL)
- Building energy certificates (CEEB)

See [phase2_outlook.md](phase2_outlook.md) for details.
