from app.schemas import (
    ComicOutline,
    ComicStory,
    ComicPanel,
)


def build_comic_layout(
    outline: ComicOutline,
    story: ComicStory,
    image_paths: list[str],
) -> list[ComicPanel]:

    story_by_number = {
        panel.panel_number: panel
        for panel in story.panels
    }

    result = []

    for index, outline_panel in enumerate(
        outline.panels
    ):

        story_panel = story_by_number.get(
            outline_panel.panel_number
        )

        if story_panel is None:
            raise ValueError(
                "Missing story data for panel "
                f"{outline_panel.panel_number}."
            )

        if index >= len(image_paths):
            raise ValueError(
                "Missing image for panel "
                f"{outline_panel.panel_number}."
            )

        result.append(
            ComicPanel(
                panel_number=outline_panel.panel_number,
                title=story_panel.title,
                image_path=image_paths[index],
                scene_description=(
                    story_panel.scene_description
                ),
                caption=story_panel.caption,
                narration=story_panel.narration,
                image_prompt=outline_panel.image_prompt,
            )
        )

    return result