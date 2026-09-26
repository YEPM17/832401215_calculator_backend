from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    database_url: str
    cors_origins: tuple[str, ...]
    max_expression_length: int = 255


def get_settings() -> Settings:
    origins = os.getenv(
        "CORS_ORIGINS",
        "http://127.0.0.1:5500,http://localhost:5500",
    )
    return Settings(
        database_url=os.getenv("DATABASE_URL", "sqlite:///./calculator.db"),
        cors_origins=tuple(
            origin.strip() for origin in origins.split(",") if origin.strip()
        ),
    )
