VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

-include .env
export

R2_ENDPOINT := https://$(CLOUDFLARE_ACCOUNT_ID).r2.cloudflarestorage.com
DUCKDB_FILE := data/ai_chat.duckdb
DBT := $(VENV)/bin/dbt --profiles-dir .

.DEFAULT_GOAL := help

.PHONY: help setup-venv install dev-install extract upload-data sync-down sync-up dbt-run dbt-docs notebook clean

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

setup-venv: ## Create the virtual environment
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip

install: ## Install production dependencies
	$(PIP) install -e .

dev-install: ## Install production + dev dependencies
	$(PIP) install -e ".[dev]"

extract: ## Extract raw JSON from zip into data/extracted/
	$(PYTHON) scripts/extract.py

upload-data: ## Upload extracted JSON files to R2
	aws s3 sync data/extracted/ s3://$(R2_BUCKET)/extracted/ \
		--endpoint-url $(R2_ENDPOINT)

sync-down: ## Pull DuckDB file from R2
	aws s3 cp s3://$(R2_BUCKET)/ai_chat.duckdb $(DUCKDB_FILE) \
		--endpoint-url $(R2_ENDPOINT) || echo "No existing DB in R2, starting fresh"

sync-up: ## Push DuckDB file to R2
	aws s3 cp $(DUCKDB_FILE) s3://$(R2_BUCKET)/ai_chat.duckdb \
		--endpoint-url $(R2_ENDPOINT)

dbt-run: install sync-down ## Run dbt models then push DB to R2
	$(DBT) run
	$(MAKE) sync-up

dbt-docs: install ## Generate and serve dbt docs (includes lineage DAG)
	$(DBT) docs generate && $(DBT) docs serve

notebook: ## Launch Jupyter notebook server
	$(VENV)/bin/jupyter notebook notebooks/

clean: ## Remove the virtual environment
	rm -rf $(VENV)
