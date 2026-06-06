"""Extract raw JSON files from the Claude export zip into data/extracted/."""

import zipfile
from pathlib import Path

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
OUT_DIR = Path(__file__).parent.parent / "data" / "extracted"

FILES_TO_EXTRACT = ["conversations.json", "users.json", "memories.json"]


def main() -> None:
    zips = list(RAW_DIR.glob("*.zip"))
    if not zips:
        raise FileNotFoundError(f"No zip files found in {RAW_DIR}")

    zip_path = zips[0]
    print(f"Extracting {zip_path.name} ...")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path) as zf:
        available = {Path(name).name: name for name in zf.namelist()}
        for filename in FILES_TO_EXTRACT:
            if filename not in available:
                print(f"  skip {filename} (not in zip)")
                continue
            dest = OUT_DIR / filename
            dest.write_bytes(zf.read(available[filename]))
            print(f"  wrote {dest.relative_to(Path.cwd())}")

    print("Done.")


if __name__ == "__main__":
    main()
