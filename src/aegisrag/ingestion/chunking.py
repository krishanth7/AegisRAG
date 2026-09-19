"""Page-aware chunking."""
import hashlib
from langchain_text_splitters import RecursiveCharacterTextSplitter
from aegisrag.ingestion.pdf import PDFPage
from aegisrag.models import DocumentChunk

def chunk_pages(pages: list[PDFPage], chunk_size: int = 900, chunk_overlap: int = 120) -> list[DocumentChunk]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks: list[DocumentChunk] = []
    for page in pages:
        for index, text in enumerate(splitter.split_text(page.text)):
            chunks.append(DocumentChunk(
                chunk_id=f"{page.document_id[:16]}-p{page.page}-c{index}",
                document_id=page.document_id, filename=page.filename, page=page.page,
                text=text, content_sha256=hashlib.sha256(text.encode()).hexdigest()
            ))
    return chunks
