from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = "ComicCraft"
    debug: bool = True

    mock_mode: bool = True

    gemini_api_key: str = ""

    outline_model: str = "gemini-3.8-flash"
    story_model: str = "gemini-3.1-pro-preview"

    hf_token: str = ""
    image_model: str = "runwayml/stable-diffusion-v1-5"
    hf_provider: str = "auto"

    max_panels: int = 5

    static_dir: Path = BASE_DIR / "static"
    templates_dir: Path = BASE_DIR / "templates"

    panels_dir: Path = BASE_DIR / "static" / "panels"
    exports_dir: Path = BASE_DIR / "static" / "exports"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    settings = Settings()

    settings.panels_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    settings.exports_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    return settings