from pathlib import Path
from ai_chat_analysis.extract_claude_chat import extract

ROOT = Path(__file__).parent.parent

if __name__ == "__main__":
    extract(
        raw_dir=ROOT / "data" / "raw",
        out_dir=ROOT / "data" / "extracted",
    )
