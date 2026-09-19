from functools import lru_cache
from aegisrag.config import get_settings
from aegisrag.services.ingestion import IngestionService
from aegisrag.services.qa import QAService
from aegisrag.services.retrieval import RetrievalService
from aegisrag.vectorstore import build_vector_store

@lru_cache
def ingestion_service() -> IngestionService:
    s=get_settings(); return IngestionService(s, build_vector_store(s))
@lru_cache
def qa_service() -> QAService:
    s=get_settings(); return QAService(s, RetrievalService(build_vector_store(s), s.top_k))
