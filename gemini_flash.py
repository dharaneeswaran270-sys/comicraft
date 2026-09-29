from app.config import get_settings
from app.schemas import (
    ComicOutline,
    PanelOutline,
    PromptRequest,
)


def _mock_outline(
    request: PromptRequest,
) -> ComicOutline:

    steps = [
        (
            "The Beginning",
            (
                f"{request.character_name} discovers "
                f"the first clue in the {request.setting}."
            ),
        ),
        (
            "Into the Unknown",
            (
                f"{request.character_name} moves deeper "
                f"into the {request.setting}, following the mystery."
            ),
        ),
        (
            "The Turning Point",
            (
                f"A surprising obstacle challenges "
                f"{request.character_name}."
            ),
        ),
        (
            "The Brave Choice",
            (
                f"{request.character_name} makes a difficult "
                f"choice and changes the course of the adventure."
            ),
        ),
        (
            "A New Dawn",
            (
                f"The adventure reaches a satisfying conclusion "
                f"in the {request.setting}."
            ),
        ),
    ]

    panels = []

    for number, (title, description) in enumerate(
        steps,
        start=1,
    ):
        image_prompt = (
            f"{request.art_style} illustration, "
            f"{request.character_name}, "
            f"{description}, "
            f"setting: {request.setting}, "
            f"tone: {request.tone}, "
            "cinematic comic panel, "
            "strong composition, "
            "expressive character"
        )

        panels.append(
            PanelOutline(
                panel_number=number,
                title=title,
                scene_description=description,
                image_prompt=image_prompt,
            )
        )

    return ComicOutline(
        panels=panels,
    )


def generate_outline(
    request: PromptRequest,
) -> ComicOutline:

    settings = get_settings()

    # Local development mode
    if settings.mock_mode:
        return _mock_outline(request)

    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is required when MOCK_MODE=false."
        )

    # Lazy import so mock mode does not require
    # an active Google client configuration.
    from google import genai
    from google.genai import types

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    prompt = f"""
Create a cohesive five-panel comic outline.

User story prompt:
{request.story_prompt}

Main character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

Requirements:

- Exactly five panels.
- Keep the named main character consistent.
- Give each panel a concise title.
- Give each panel a vivid scene description.
- Give each panel a standalone image-generation prompt.
- The sequence must have a beginning.
- Include escalation.
- Include a turning point.
- Include a conclusion.
- Do not include markdown fences.
"""

    response = client.models.generate_content(
        model=settings.outline_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ComicOutline,
            temperature=0.9,
        ),
    )

    return ComicOutline.model_validate_json(
        response.text
    )