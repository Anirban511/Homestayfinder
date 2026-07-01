"""Application settings loaded from environment variables."""
import os
from functools import lru_cache


class Settings:
    # Database. Defaults to local SQLite; set DATABASE_URL to Postgres in prod.
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./homestay.db")

    # Auth
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-only-secret-change-me")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

    # CORS. CLIENT_URLS accepts a comma-separated list so local dev, Vercel
    # preview deployments, and the production Vercel URL can all be allowed at
    # once. CLIENT_URL (singular) is kept as a fallback for existing setups.
    CLIENT_URLS: str = os.getenv("CLIENT_URLS", os.getenv("CLIENT_URL", "http://localhost:3000"))

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.CLIENT_URLS.split(",") if origin.strip()]

    # Payment service toggle. "stub" returns fake successful payments so the app
    # runs with no Stripe account; "real" would call the Stripe API.
    PAYMENT_MODE: str = os.getenv("PAYMENT_MODE", "stub")
    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", "")

    # Rate limiting (requests per window per client).
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_WINDOW_SECONDS: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
