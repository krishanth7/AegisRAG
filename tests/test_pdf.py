from pathlib import Path
import pytest
from aegisrag.ingestion.pdf import PDFValidationError,load_pdf
def test_rejects_non_pdf(tmp_path:Path)->None:
    p=tmp_path/"report.txt"; p.write_text("text")
    with pytest.raises(PDFValidationError): load_pdf(p,1024)
def test_rejects_oversized_pdf(tmp_path:Path)->None:
    p=tmp_path/"large.pdf"; p.write_bytes(b"x"*10)
    with pytest.raises(PDFValidationError): load_pdf(p,5)
