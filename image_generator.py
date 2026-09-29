from pathlib import Path
import hashlib
import re

from PIL import Image, ImageDraw

from app.config import get_settings


def _safe_name(prompt: str) -> str:

    slug = re.sub(
        r"[^a-zA-Z0-9]+",
        "-",
        prompt.lower(),
    ).strip("-")

    digest = hashlib.sha1(
        prompt.encode("utf-8")
    ).hexdigest()[:10]

    return (
        f"{slug[:50] or 'panel'}-"
        f"{digest}.png"
    )


def _mock_image(
    prompt: str,
    output: Path,
) -> None:

    image = Image.new(
        "RGB",
        (1024, 768),
        "white",
    )

    draw = ImageDraw.Draw(image)

    draw.rectangle(
        (25, 25, 999, 743),
        outline="black",
        width=8,
    )

    draw.text(
        (60, 80),
        "COMICCRAFT DEMO IMAGE",
        fill="black",
    )

    # Keep the demo image readable even with
    # a very long generated prompt.
    preview = prompt[:300]

    draw.text(
        (60, 150),
        preview,
        fill="black",
    )

    image.save(output)


def generate_image(
    prompt: str,
) -> str:

    settings = get_settings()

    output = (
        settings.panels_dir
        / _safe_name(prompt)
    )

    # Development/demo mode
    if settings.mock_mode:

        _mock_image(
            prompt,
            output,
        )

        return (
            f"/static/panels/"
            f"{output.name}"
        )

    if not settings.hf_token:
        raise RuntimeError(
            "HF_TOKEN is required when "
            "MOCK_MODE=false."
        )

    # Lazy import.
    from huggingface_hub import InferenceClient

    client = InferenceClient(
        provider=settings.hf_provider,
        api_key=settings.hf_token,
    )

    image = client.text_to_image(
        prompt=prompt,
        model=settings.image_model,
    )

    image.save(output)

    return (
        f"/static/panels/"
        f"{output.name}"
    )