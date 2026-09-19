"""Ingestion orchestration."""
from pathlib import Path
from langchain_chroma import Chroma
from aegisrag.config import Settings
from aegisrag.ingestion.chunking import chunk_pages
from aegisrag.ingestion.pdf import load_pdf
from aegisrag.vectorstore import upsert_chunks

class IngestionService:
    def __init__(self, settings: Settings, store: Chroma) -> None:
        self.settings, self.store = settings, store
    def ingest(self, path: Path) -> dict[str, object]:
        pages = load_pdf(path, self.settings.max_upload_mb * 1024 * 1024)
        ids = upsert_chunks(self.store, chunk_pages(pages))
        return {"document_id": pages[0].document_id, "filename": path.name, "pages": len(pages), "chunks": len(ids)}
