import sys
from pathlib import Path

from ai_chat_analysis import config as cfg
from ai_chat_analysis.extract_claude_chat import extract
from ai_chat_analysis.r2 import R2Client
from ai_chat_analysis.settings import R2Settings

ROOT = Path(__file__).parent.parent


def main() -> None:
    conf = cfg.load()
    client = R2Client(R2Settings())

    print("Verifying R2 credentials...")
    try:
        client.verify()
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    tmp_raw = ROOT / conf.claude_chat_local_tmp_dir / "raw"
    tmp_out = ROOT / conf.claude_chat_local_tmp_dir / "extracted"

    print(f"Downloading {conf.claude_chat_r2_raw_prefix}/ from R2...")
    tmp_raw.mkdir(parents=True, exist_ok=True)
    count = client.download_prefix(conf.claude_chat_r2_raw_prefix, tmp_raw)
    print(f"Downloaded {count} files.")

    print("Extracting...")
    extract(raw_dir=tmp_raw, out_dir=tmp_out)

    print(f"Uploading extracted files to {conf.claude_chat_r2_output_prefix}/ in R2...")
    uploaded, skipped = client.sync_dir(tmp_out, conf.claude_chat_r2_output_prefix)
    print(f"Done. {uploaded} uploaded, {skipped} unchanged.")


if __name__ == "__main__":
    main()
