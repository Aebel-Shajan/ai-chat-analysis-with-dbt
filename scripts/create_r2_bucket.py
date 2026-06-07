import sys
from ai_chat_analysis.r2 import R2Client
from ai_chat_analysis.settings import R2Settings


def main() -> None:
    client = R2Client(R2Settings())

    print("Verifying R2 credentials...")
    try:
        client.verify()
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    print("Credentials OK.")

    if client.bucket_exists():
        print(f"Bucket '{client.bucket}' already exists.")
        return

    print(f"Creating bucket '{client.bucket}'...")
    try:
        client.create_bucket()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    print("Done.")


if __name__ == "__main__":
    main()
