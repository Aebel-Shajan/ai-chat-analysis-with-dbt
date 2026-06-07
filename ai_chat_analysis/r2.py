import hashlib
from pathlib import Path

import boto3
import requests
from botocore.exceptions import ClientError, NoCredentialsError

from ai_chat_analysis.settings import R2Settings


class R2Client:
    def __init__(self, settings: R2Settings) -> None:
        self._settings = settings
        self._s3 = boto3.client(
            "s3",
            endpoint_url=settings.endpoint_url,
            aws_access_key_id=settings.r2_access_key_id,
            aws_secret_access_key=settings.r2_secret_access_key,
            region_name="auto",
        )

    @property
    def bucket(self) -> str:
        return self._settings.r2_bucket

    def verify(self) -> None:
        """Raise if S3 credentials are invalid or cannot reach R2."""
        try:
            self._s3.list_buckets()
        except NoCredentialsError:
            raise ValueError("R2 credentials are missing or malformed")
        except ClientError as e:
            code = e.response["Error"]["Code"]
            raise ValueError(f"R2 credentials rejected ({code}): {e}")

    def bucket_exists(self) -> bool:
        try:
            self._s3.head_bucket(Bucket=self.bucket)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] in ("404", "NoSuchBucket"):
                return False
            raise

    def create_bucket(self) -> None:
        """Create the bucket via the Cloudflare REST API (requires API token)."""
        s = self._settings
        url = f"https://api.cloudflare.com/client/v4/accounts/{s.cloudflare_account_id}/r2/buckets"
        resp = requests.post(
            url,
            headers={"Authorization": f"Bearer {s.cloudflare_api_token}"},
            json={"name": self.bucket},
        )
        resp.raise_for_status()
        data = resp.json()
        if not data.get("success"):
            raise RuntimeError(f"Failed to create bucket: {data.get('errors', [])}")

    def upload_file(self, local_path: Path, key: str) -> None:
        self._s3.upload_file(str(local_path), self.bucket, key)

    def download_file(self, key: str, local_path: Path) -> None:
        local_path.parent.mkdir(parents=True, exist_ok=True)
        self._s3.download_file(self.bucket, key, str(local_path))

    def object_etag(self, key: str) -> str | None:
        """Return the ETag of an R2 object, or None if it doesn't exist."""
        try:
            head = self._s3.head_object(Bucket=self.bucket, Key=key)
            return head["ETag"].strip('"')
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return None
            raise

    def download_prefix(self, prefix: str, local_dir: Path) -> int:
        """Download all objects under prefix into local_dir. Returns file count."""
        paginator = self._s3.get_paginator("list_objects_v2")
        count = 0
        for page in paginator.paginate(Bucket=self.bucket, Prefix=prefix):
            for obj in page.get("Contents", []):
                key = obj["Key"]
                relative = key[len(prefix):].lstrip("/")
                dest = local_dir / relative
                self.download_file(key, dest)
                print(f"  downloaded {key}")
                count += 1
        return count

    def sync_dir(self, local_dir: Path, prefix: str) -> tuple[int, int]:
        """Upload files under local_dir to R2 prefix, skipping unchanged files.

        Returns (uploaded, skipped) counts.
        """
        files = [f for f in local_dir.rglob("*") if f.is_file()]
        uploaded = skipped = 0

        for local_path in sorted(files):
            key = f"{prefix}/{local_path.relative_to(local_dir)}"
            local_md5 = hashlib.md5(local_path.read_bytes()).hexdigest()

            if self.object_etag(key) == local_md5:
                skipped += 1
                continue

            self.upload_file(local_path, key)
            print(f"  uploaded {key}")
            uploaded += 1

        return uploaded, skipped
