#!/bin/sh
# Wrapper so launchctl picks up .env credentials before running the sync.
set -e

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [ -f "$REPO_DIR/.env" ]; then
    set -a
    . "$REPO_DIR/.env"
    set +a
fi

exec "$REPO_DIR/.venv/bin/python" "$REPO_DIR/scripts/sync_cc_projects_folder.py"
