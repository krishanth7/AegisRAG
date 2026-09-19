"""Persistent vector storage."""
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from aegisrag.config import Settings
from aegisrag.models import DocumentChunk

def build_vector_store(settings: Settings) -> Chroma:
    settings.chroma_path.mkdir(parents=True, exist_ok=True)
    return Chroma(collection_name=settings.collection, persist_directory=str(settings.chroma_path), embedding_function=OpenAIEmbeddings(model=settings.embedding_model), collection_metadata={"hnsw:space": "cosine"})

def upsert_chunks(store: Chroma, chunks: list[DocumentChunk]) -> list[str]:
    documents = [Document(page_content=c.text, metadata={"document_id": c.document_id, "filename": c.filename, "page": c.page, "chunk_id": c.chunk_id, "content_sha256": c.content_sha256}) for c in chunks]
    ids = [c.chunk_id for c in chunks]
    if documents:
        store.add_documents(documents=documents, ids=ids)
    return ids
