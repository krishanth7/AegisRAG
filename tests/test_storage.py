from pathlib import Path
import pytest
from aegisrag.storage import UploadValidationError, allocate_upload_path

def test_paths_are_unique(tmp_path: Path) -> None:
    assert allocate_upload_path(tmp_path, "report.pdf") != allocate_upload_path(tmp_path, "report.pdf")

def test_traversal_is_removed(tmp_path: Path) -> None:
    result = allocate_upload_path(tmp_path, "../../board report.pdf")
    assert result.parent == tmp_path and ".." not in result.name

def test_non_pdf_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(UploadValidationError):
        allocate_upload_path(tmp_path, "payload.exe")
