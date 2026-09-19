"""Semantic retrieval."""
from dataclasses import dataclass
from langchain_chroma import Chroma
from langchain_core.documents import Document

@dataclass(frozen=True)
class RetrievedDocument:
    document: Document
    relevance: float

class RetrievalService:
    def __init__(self, store: Chroma, default_top_k: int = 5) -> None:
        self.store, self.default_top_k = store, default_top_k
    def search(self, query: str, top_k: int | None = None) -> list[RetrievedDocument]:
        return [RetrievedDocument(document=d, relevance=float(s)) for d, s in self.store.similarity_search_with_relevance_scores(query, k=top_k or self.default_top_k)]
