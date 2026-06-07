VENV   := .venv
PYTHON := $(VENV)/bin/python
PIP    := $(VENV)/bin/pip
DBT    := $(VENV)/bin/dbt --project-dir dbt --profiles-dir dbt

-include .env
export

.DEFAULT_GOAL := help

.PHONY: help setup-venv install extract create-bucket set-gh-secrets dbt-run dbt-docs clean

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

setup-venv: ## Create the virtual environment
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip

install: ## Install production + dev dependencies
	$(PIP) install -e ".[dev]"

extract: ## Extract raw JSON from zip into data/extracted/
	$(PYTHON) scripts/extract_claude_chat.py
	$(PYTHON) scripts/extract_claude_code.py

create-bucket: ## Create R2 bucket if it doesn't exist
	$(PYTHON) scripts/create_r2_bucket.py

set-gh-secrets: ## Set GitHub secrets from .env
	sh scripts/set_gh_secrets.sh

dbt-run: ## Run all dbt models
	$(DBT) run

dbt-docs: ## Generate and serve dbt docs (includes lineage DAG)
	$(DBT) docs generate && $(DBT) docs serve

clean: ## Remove the virtual environment
	rm -rf $(VENV)
