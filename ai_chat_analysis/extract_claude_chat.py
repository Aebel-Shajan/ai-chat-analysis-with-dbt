import zipfile
from pathlib import Path

FILES_TO_EXTRACT = ["conversations.json", "users.json", "memories.json"]


def extract(raw_dir: Path, out_dir: Path) -> None:
    zips = list(raw_dir.glob("*.zip"))
    if not zips:
        raise FileNotFoundError(f"No zip files found in {raw_dir}")

    zip_path = zips[0]
    print(f"Extracting {zip_path.name} ...")

    out_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path) as zf:
        available = {Path(name).name: name for name in zf.namelist()}
        for filename in FILES_TO_EXTRACT:
            if filename not in available:
                print(f"  skip {filename} (not in zip)")
                continue
            dest = out_dir / filename
            dest.write_bytes(zf.read(available[filename]))
            print(f"  wrote {dest}")

    print("Done.")
