from typing import List

from pydantic import BaseModel, Field, field_validator


class PromptRequest(BaseModel):
    story_prompt: str = Field(
        ...,
        min_length=5,
        max_length=2000,
    )

    character_name: str = Field(
        ...,
        min_length=1,
        max_length=80,
    )

    setting: str = Field(
        ...,
        min_length=1,
        max_length=120,
    )

    tone: str = Field(
        ...,
        min_length=1,
        max_length=80,
    )

    art_style: str = Field(
        ...,
        min_length=1,
        max_length=120,
    )

    @field_validator("*")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()


class PanelOutline(BaseModel):
    panel_number: int = Field(
        ...,
        ge=1,
    )

    title: str

    scene_description: str

    image_prompt: str


class ComicOutline(BaseModel):
    panels: List[PanelOutline]


class PanelStory(BaseModel):
    panel_number: int = Field(
        ...,
        ge=1,
    )

    title: str

    scene_description: str

    caption: str

    narration: str


class ComicStory(BaseModel):
    panels: List[PanelStory]


class ComicPanel(BaseModel):
    panel_number: int

    title: str

    image_path: str

    scene_description: str

    caption: str

    narration: str

    image_prompt: str


class ImageRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=5,
        max_length=4000,
    )


class ComicResponse(BaseModel):
    success: bool

    layout: List[ComicPanel]

    pdf_path: str