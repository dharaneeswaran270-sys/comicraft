from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.routes import router


settings = get_settings()


app = FastAPI(
    title=settings.app_name,
    description="AI-powered comic story creator.",
    version="1.0.0",
)


app.mount(
    "/static",
    StaticFiles(
        directory=str(
            settings.static_dir
        )
    ),
    name="static",
)


app.include_router(
    router
)


@app.get("/health")
async def health():

    return {
        "status": "ok",
        "mock_mode": settings.mock_mode,
        "outline_model": settings.outline_model,
        "story_model": settings.story_model,
        "image_model": settings.image_model,
    }