from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    database_url: str = "sqlite:///./openbook.db"
    redis_url: str = "redis://localhost:6379/0"
    cors_origins: str = "http://localhost:8080"
    secret_key: str = "dev-only-change-me"
    access_token_minutes: int = 60 * 12
    trial_days: int = 14

    @property
    def cors_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    def validate_for_production(self) -> None:
        if self.app_env == "production" and (self.secret_key == "dev-only-change-me" or len(self.secret_key) < 32):
            raise RuntimeError("SECRET_KEY must be set to a random value of at least 32 characters in production")


settings = Settings()
settings.validate_for_production()
