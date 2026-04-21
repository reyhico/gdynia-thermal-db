.PHONY: help install install-dev lint format test clean fetch-buildings fetch-districts build-database

PYTHON := python
PIP := pip

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install:  ## Install package in editable mode
	$(PIP) install -e .

install-dev:  ## Install package with dev dependencies
	$(PIP) install -e ".[dev]"
	pre-commit install

lint:  ## Run linters
	ruff check src/ tests/
	mypy src/

format:  ## Format code
	ruff format src/ tests/
	ruff check --fix src/ tests/

test:  ## Run tests
	pytest tests/ -v

test-cov:  ## Run tests with coverage
	pytest tests/ -v --cov=gdynia_thermal_db --cov-report=html --cov-report=term

clean:  ## Clean build artifacts and caches
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache/ .mypy_cache/ htmlcov/ .coverage

# Data pipeline commands
audit-viewer:  ## Audit the viewer and inventory resources
	gdynia-thermal audit-viewer

fetch-buildings:  ## Download the building GeoJSON
	gdynia-thermal fetch-buildings

fetch-viewer-assets:  ## Download viewer configuration assets
	gdynia-thermal fetch-viewer-assets

fetch-districts:  ## Download the Gdynia district boundaries ZIP
	gdynia-thermal fetch-districts

import-districts:  ## Import and process district boundaries
	gdynia-thermal import-districts

build-grid:  ## Build fallback grid if districts unavailable
	gdynia-thermal build-grid

process-buildings:  ## Process and clean building data
	gdynia-thermal process-buildings

inventory-thermal:  ## Inventory thermal tile resources
	gdynia-thermal inventory-thermal-tiles

build-database:  ## Build master database tables
	gdynia-thermal build-database

compute-metrics:  ## Compute district-level metrics
	gdynia-thermal compute-district-metrics

export-data:  ## Export data products
	gdynia-thermal export-data

# Full pipeline
pipeline: fetch-buildings fetch-districts import-districts process-buildings build-database compute-metrics  ## Run full data pipeline
