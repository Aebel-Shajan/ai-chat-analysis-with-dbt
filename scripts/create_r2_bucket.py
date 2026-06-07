"""Create the R2 bucket if it doesn't already exist."""

import sys
from ai_chat_analysis.settings import R2Settings


def main() -> None:
    settings = R2Settings()

    print("Verifying R2 credentials...")
    try:
        settings.verify()
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    print("Credentials OK.")

    if settings.bucket_exists():
        print(f"Bucket '{settings.r2_bucket}' already exists.")
        return

    print(f"Creating bucket '{settings.r2_bucket}'...")
    try:
        settings.create_bucket()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    print("Done.")


if __name__ == "__main__":
    main()
