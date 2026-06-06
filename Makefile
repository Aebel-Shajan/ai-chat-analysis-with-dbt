VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.DEFAULT_GOAL := help

.PHONY: help venv install dev-install extract dbt-run dbt-docs notebook clean

DBT := $(VENV)/bin/dbt 

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

setup-venv: ## Create the virtual environment
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip

install:  ## Install production dependencies
	$(PIP) install -e .

dev-install:  ## Install production + dev dependencies
	$(PIP) install -e ".[dev]"

extract:  ## Extract raw JSON from zip into data/extracted/
	$(PYTHON) scripts/extract.py

dbt-docs:  ## Generate and serve dbt docs (includes lineage DAG)
	$(DBT) docs generate && $(DBT) docs serve

dbt-run:  ## Run all dbt models
	$(DBT) run

notebook: ## Launch Jupyter notebook server
	$(VENV)/bin/jupyter notebook notebooks/

clean: ## Remove the virtual environment
	rm -rf $(VENV)
