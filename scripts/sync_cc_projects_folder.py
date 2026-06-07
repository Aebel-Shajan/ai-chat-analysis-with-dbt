"""Sync ~/.claude/projects/ to R2 under the claude_code/projects/ prefix."""

import sys
from pathlib import Path

from ai_chat_analysis.r2 import R2Client
from ai_chat_analysis.settings import R2Settings

CLAUDE_PROJECTS = Path.home() / ".claude" / "projects"
R2_PREFIX = "claude_code/projects"


def main() -> None:
    client = R2Client(R2Settings())

    print("Verifying R2 credentials...")
    try:
        client.verify()
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    if not CLAUDE_PROJECTS.exists():
        print(f"ERROR: {CLAUDE_PROJECTS} does not exist")
        sys.exit(1)

    print(f"Syncing {CLAUDE_PROJECTS} -> r2://{client.bucket}/{R2_PREFIX}")
    uploaded, skipped = client.sync_dir(CLAUDE_PROJECTS, R2_PREFIX)
    print(f"Done. {uploaded} uploaded, {skipped} unchanged.")


if __name__ == "__main__":
    main()
