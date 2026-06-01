VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.DEFAULT_GOAL := help

.PHONY: help venv install dev-install clean

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

venv: ## Create the virtual environment
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip

install: venv ## Install production dependencies
	$(PIP) install -e .

dev-install: venv ## Install production + dev dependencies
	$(PIP) install -e ".[dev]"

clean: ## Remove the virtual environment
	rm -rf $(VENV)
