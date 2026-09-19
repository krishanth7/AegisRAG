"""Safe PDF extraction."""
import hashlib
from dataclasses import dataclass
from pathlib import Path
from pypdf import PdfReader

class PDFValidationError(ValueError):
    pass

@dataclass(frozen=True)
class PDFPage:
    document_id: str
    filename: str
    page: int
    text: str

def load_pdf(path: Path, max_bytes: int) -> list[PDFPage]:
    if path.suffix.lower() != ".pdf":
        raise PDFValidationError("Only PDF documents are supported.")
    if not path.is_file():
        raise PDFValidationError("Document does not exist.")
    if path.stat().st_size > max_bytes:
        raise PDFValidationError("Document exceeds the configured upload limit.")
    raw = path.read_bytes()
    document_id = hashlib.sha256(raw).hexdigest()
    reader = PdfReader(path)
    if reader.is_encrypted:
        raise PDFValidationError("Encrypted PDFs are not supported.")
    pages = [PDFPage(document_id, path.name, i, text.strip()) for i, page in enumerate(reader.pages, 1) if (text := (page.extract_text() or "")).strip()]
    if not pages:
        raise PDFValidationError("No extractable text was found.")
    return pages
