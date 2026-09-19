from aegisrag.ingestion.chunking import chunk_pages
from aegisrag.ingestion.pdf import PDFPage
def test_chunks_preserve_provenance()->None:
    chunks=chunk_pages([PDFPage("a"*64,"risk.pdf",3,"Revenue increased. "*100)],120,20)
    assert len(chunks)>1
    assert all(c.filename=="risk.pdf" and c.page==3 for c in chunks)
    assert len({c.chunk_id for c in chunks})==len(chunks)
