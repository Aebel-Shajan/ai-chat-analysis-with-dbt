from pydantic_settings import BaseSettings, SettingsConfigDict


class R2Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    cloudflare_account_id: str
    cloudflare_api_token: str | None = None  # Workers R2 Storage:Edit permission, only needed for create_r2_bucket.py
    r2_access_key_id: str
    r2_secret_access_key: str
    r2_bucket: str

    @property
    def endpoint_url(self) -> str:
        return f"https://{self.cloudflare_account_id}.r2.cloudflarestorage.com"
