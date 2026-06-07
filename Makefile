VENV   := .venv
PYTHON := $(VENV)/bin/python
PIP    := $(VENV)/bin/pip
DBT    := $(VENV)/bin/dbt --project-dir dbt --profiles-dir dbt

-include .env
export

.DEFAULT_GOAL := help

REPO_DIR     := $(shell pwd)
PLIST_SRC    := launchctl/com.aebel.sync-claude-code.plist
PLIST_DEST   := $(HOME)/Library/LaunchAgents/com.aebel.sync-claude-code.plist
LAUNCH_LABEL := com.aebel.sync-claude-code

.PHONY: help setup-venv install extract create-bucket set-gh-secrets dbt-run dbt-docs \
        sync-claude-code install-sync-cron uninstall-sync-cron clean

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

sync-claude-code: ## Manually run the Claude Code → R2 sync
	$(PYTHON) scripts/sync_cc_projects_folder.py

install-sync-cron: ## Install launchctl agent (runs sync every hour)
	chmod +x launchctl/sync_cc_projects_folder.sh
	sed "s|REPO_DIR|$(REPO_DIR)|g" $(PLIST_SRC) > $(PLIST_DEST)
	launchctl load -w $(PLIST_DEST)
	@echo "Installed: runs every hour. Logs → logs/sync_cc_projects_folder.{log,err}"

uninstall-sync-cron: ## Remove launchctl agent
	launchctl unload -w $(PLIST_DEST)
	rm -f $(PLIST_DEST)
	@echo "Uninstalled."

clean: ## Remove the virtual environment
	rm -rf $(VENV)
