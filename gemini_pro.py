from app.config import get_settings
from app.schemas import (
    ComicOutline,
    ComicStory,
    PanelStory,
    PromptRequest,
)


def _mock_story(
    request: PromptRequest,
    outline: ComicOutline,
) -> ComicStory:

    panels = []

    for panel in outline.panels:

        panels.append(
            PanelStory(
                panel_number=panel.panel_number,
                title=panel.title,
                scene_description=panel.scene_description,
                caption=(
                    f"The {request.setting} falls quiet "
                    "as the next moment unfolds."
                ),
                narration=(
                    f"{request.character_name}: "
                    "This is not the end of the story. "
                    "I have to keep going."
                ),
            )
        )

    return ComicStory(
        panels=panels,
    )


def generate_story(
    request: PromptRequest,
    outline: ComicOutline,
) -> ComicStory:

    settings = get_settings()

    if settings.mock_mode:
        return _mock_story(
            request,
            outline,
        )

    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is required when MOCK_MODE=false."
        )

    from google import genai
    from google.genai import types

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    prompt = f"""
Expand this five-panel outline into polished
comic narration and dialogue.

User preferences:

Main character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

Original story prompt:
{request.story_prompt}

Outline:
{outline.model_dump_json(indent=2)}

Requirements:

- Return exactly five story panels.
- Match the panel numbers.
- Preserve the panel titles.
- Preserve the scene descriptions.
- Add a short ambient caption.
- Add engaging narration or dialogue.
- Keep character voice consistent.
- Keep story continuity consistent.
- Do not add extra panels.
- Do not use markdown.
"""

    response = client.models.generate_content(
        model=settings.story_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ComicStory,
            temperature=0.95,
        ),
    )

    return ComicStory.model_validate_json(
        response.text
    )