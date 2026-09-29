from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from fpdf import FPDF

from app.config import get_settings
from app.schemas import ComicPanel


def _pdf_text(
    value: str,
) -> str:

    # FPDF's built-in Helvetica font is Latin-1.
    # Replace unsupported Unicode characters safely.
    return (
        value
        .encode("latin-1", "replace")
        .decode("latin-1")
    )


def _image_from_url(
    image_path: str,
) -> Path:

    settings = get_settings()

    name = Path(
        urlparse(image_path).path
    ).name

    candidate = (
        settings.panels_dir
        / name
    )

    if not candidate.exists():
        raise FileNotFoundError(
            f"Generated image not found: "
            f"{candidate}"
        )

    return candidate


def save_pdf(
    layout: list[ComicPanel],
) -> str:

    settings = get_settings()

    timestamp = datetime.now().strftime(
        "%Y%m%d-%H%M%S-%f"
    )

    output = (
        settings.exports_dir
        / f"comiccraft-{timestamp}.pdf"
    )

    pdf = FPDF(
        format="A4"
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=16,
    )

    for panel in layout:

        pdf.add_page()

        pdf.set_font(
            "Helvetica",
            "B",
            18,
        )

        pdf.multi_cell(
            0,
            10,
            (
                f"Panel {panel.panel_number}: "
                f"{_pdf_text(panel.title)}"
            ),
        )

        pdf.ln(3)

        image = _image_from_url(
            panel.image_path
        )

        pdf.image(
            str(image),
            x=15,
            y=40,
            w=180,
        )

        pdf.set_y(145)

        pdf.set_font(
            "Helvetica",
            "I",
            11,
        )

        pdf.multi_cell(
            0,
            7,
            _pdf_text(
                panel.scene_description
            ),
        )

        pdf.ln(2)

        pdf.set_font(
            "Helvetica",
            "B",
            11,
        )

        pdf.multi_cell(
            0,
            7,
            (
                "Caption: "
                f"{_pdf_text(panel.caption)}"
            ),
        )

        pdf.ln(2)

        pdf.set_font(
            "Helvetica",
            "",
            11,
        )

        pdf.multi_cell(
            0,
            7,
            _pdf_text(
                panel.narration
            ),
        )

    pdf.output(
        str(output)
    )

    return (
        f"/static/exports/"
        f"{output.name}"
    )