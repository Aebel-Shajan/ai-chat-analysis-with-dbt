import sys
from pathlib import Path

from ai_chat_analysis import config as cfg
from ai_chat_analysis.extract_claude_code import extract
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

    tmp_projects = ROOT / conf.claude_code_local_tmp_dir / "projects"
    tmp_out = ROOT / conf.claude_code_local_tmp_dir / "out"

    print(f"Downloading {conf.claude_code_r2_projects_prefix}/ from R2...")
    tmp_projects.mkdir(parents=True, exist_ok=True)
    count = client.download_prefix(conf.claude_code_r2_projects_prefix, tmp_projects)
    print(f"Downloaded {count} files.")

    print("Extracting...")
    tmp_out.mkdir(parents=True, exist_ok=True)
    extract(projects_dir=tmp_projects, out_dir=tmp_out)

    output_file = tmp_out / "messages.jsonl"
    print(f"Uploading to {conf.claude_code_r2_output_key} in R2...")
    client.upload_file(output_file, conf.claude_code_r2_output_key)
    print("Done.")


if __name__ == "__main__":
    main()
