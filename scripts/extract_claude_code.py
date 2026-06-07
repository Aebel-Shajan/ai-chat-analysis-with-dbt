from pathlib import Path
from ai_chat_analysis.extract_claude_code import extract

ROOT = Path(__file__).parent.parent

if __name__ == "__main__":
    extract(
        projects_dir=Path.home() / ".claude" / "projects",
        out_dir=ROOT / "data" / "extracted" / "claude_code",
    )
