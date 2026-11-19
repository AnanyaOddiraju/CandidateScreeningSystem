import pymupdf
from docx import Document
from pathlib import Path
from io import BytesIO


ALLOWED_EXTENSIONS = {".pdf", ".docx"}


def extract_resume(
    file_bytes: bytes,
    filename: str
) -> str:

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported resume format")

    if extension == ".pdf":

        with pymupdf.open(
            stream=file_bytes,
            filetype="pdf"
        ) as pdf:

            text = "\n".join(
                page.get_text("text")
                for page in pdf
            )

    elif extension == ".docx":

        document = Document(
            BytesIO(file_bytes)
        )

        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

        for table in document.tables:
            for row in table.rows:
                text += "\n" + " | ".join(
                    cell.text for cell in row.cells
                )

    text = text.strip()

    if not text:
        raise ValueError(
            "No readable text found in resume"
        )

    return text