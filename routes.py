from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request,
)

from fastapi.responses import HTMLResponse

from fastapi.templating import (
    Jinja2Templates,
)

from app.config import get_settings

from app.schemas import (
    ComicResponse,
    ImageRequest,
    PromptRequest,
)

from services.exporters import (
    save_pdf,
)

from services.gemini_flash import (
    generate_outline,
)

from services.gemini_pro import (
    generate_story,
)

from services.image_generator import (
    generate_image,
)

from services.layout_builder import (
    build_comic_layout,
)


router = APIRouter()

settings = get_settings()

templates = Jinja2Templates(
    directory=str(
        settings.templates_dir
    )
)


def generate_comic(
    request_data: PromptRequest,
):

    # STEP 1:
    # Generate five-panel outline.
    outline = generate_outline(
        request_data
    )

    # STEP 2:
    # Generate dialogue/narration.
    story = generate_story(
        request_data,
        outline,
    )

    # STEP 3:
    # Generate one image per panel.
    image_paths = []

    for panel in outline.panels:

        image_path = generate_image(
            panel.image_prompt
        )

        image_paths.append(
            image_path
        )

    # STEP 4:
    # Combine generated assets.
    layout = build_comic_layout(
        outline,
        story,
        image_paths,
    )

    # STEP 5:
    # Generate downloadable PDF.
    pdf_path = save_pdf(
        layout
    )

    return layout, pdf_path


@router.get(
    "/",
    response_class=HTMLResponse,
)
async def home(
    request: Request,
):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": settings.app_name,
        },
    )


@router.get(
    "/generate",
    response_class=HTMLResponse,
)
async def generate_get(
    request: Request,
):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": settings.app_name,
        },
    )


@router.post(
    "/generate",
    response_class=HTMLResponse,
)
async def generate_form(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):

    try:

        data = PromptRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )

        layout, pdf_path = (
            generate_comic(data)
        )

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "title": "Comic Preview",
                "layout": layout,
                "pdf_path": pdf_path,
            },
        )

    except Exception as exc:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "title": settings.app_name,
                "error": str(exc),
            },
            status_code=500,
        )


@router.post(
    "/generate-comic/json",
    response_model=ComicResponse,
)
async def generate_json(
    payload: PromptRequest,
):

    try:

        layout, pdf_path = (
            generate_comic(payload)
        )

        return ComicResponse(
            success=True,
            layout=layout,
            pdf_path=pdf_path,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@router.post(
    "/test-image",
)
async def test_image(
    payload: ImageRequest,
):

    try:

        image_path = generate_image(
            payload.prompt
        )

        return {
            "success": True,
            "image_path": image_path,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@router.get(
    "/export-success",
    response_class=HTMLResponse,
)
async def export_success(
    request: Request,
    pdf: str | None = None,
):

    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={
            "title": "Export Successful",
            "pdf_path": pdf,
        },
    )