"""Secure upload staging."""
import re
from pathlib import Path
from uuid import uuid4
_SAFE_NAME = re.compile(r"[^A-Za-z0-9._-]+")
class UploadValidationError(ValueError): pass

def allocate_upload_path(upload_dir: Path, original_filename: str) -> Path:
    basename = Path(original_filename).name
    sanitized = _SAFE_NAME.sub("-", basename).strip(".-")
    if not sanitized.lower().endswith(".pdf"):
        raise UploadValidationError("Only .pdf uploads are accepted.")
    stem = Path(sanitized).stem[:80] or "report"
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir / f"{stem}-{uuid4().hex}.pdf"
