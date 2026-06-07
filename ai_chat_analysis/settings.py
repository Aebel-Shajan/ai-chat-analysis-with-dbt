import boto3
import requests
from botocore.exceptions import ClientError, NoCredentialsError
from pydantic_settings import BaseSettings, SettingsConfigDict


class R2Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    cloudflare_account_id: str
    cloudflare_api_token: str  # needs Workers R2 Storage:Edit permission
    r2_access_key_id: str
    r2_secret_access_key: str
    r2_bucket: str

    @property
    def endpoint_url(self) -> str:
        return f"https://{self.cloudflare_account_id}.r2.cloudflarestorage.com"

    def client(self):
        return boto3.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.r2_access_key_id,
            aws_secret_access_key=self.r2_secret_access_key,
            region_name="auto",
        )

    def verify(self) -> None:
        """Raise if S3 credentials are invalid or cannot reach R2."""
        try:
            self.client().list_buckets()
        except NoCredentialsError:
            raise ValueError("R2 credentials are missing or malformed")
        except ClientError as e:
            code = e.response["Error"]["Code"]
            raise ValueError(f"R2 credentials rejected ({code}): {e}")

    def bucket_exists(self) -> bool:
        try:
            self.client().head_bucket(Bucket=self.r2_bucket)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] in ("404", "NoSuchBucket"):
                return False
            raise

    def create_bucket(self) -> None:
        """Create the bucket via the Cloudflare REST API (requires API token)."""
        url = f"https://api.cloudflare.com/client/v4/accounts/{self.cloudflare_account_id}/r2/buckets"
        resp = requests.post(
            url,
            headers={"Authorization": f"Bearer {self.cloudflare_api_token}"},
            json={"name": self.r2_bucket},
        )
        resp.raise_for_status()
        data = resp.json()
        if not data.get("success"):
            errors = data.get("errors", [])
            raise RuntimeError(f"Failed to create bucket: {errors}")
