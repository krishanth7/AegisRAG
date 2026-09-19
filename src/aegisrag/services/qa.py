"""Grounded question answering."""
from uuid import uuid4
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from aegisrag.config import Settings
from aegisrag.models import AnswerResponse, Citation
from aegisrag.services.retrieval import RetrievalService

SYSTEM_PROMPT = """Answer only from supplied report excerpts. If unsupported, say the reports do not contain enough information. Never invent facts. Cite [filename, p. N]."""

class QAService:
    def __init__(self, settings: Settings, retrieval: RetrievalService) -> None:
        self.retrieval = retrieval
        self.chain = ChatPromptTemplate.from_messages([("system", SYSTEM_PROMPT), ("human", "Context:\n{context}\n\nQuestion: {question}")]) | ChatOpenAI(model=settings.chat_model, temperature=0)
    def answer(self, question: str, top_k: int | None = None) -> AnswerResponse:
        matches = self.retrieval.search(question, top_k)
        context = "\n\n".join(f"[{m.document.metadata['filename']}, p. {m.document.metadata['page']}]\n{m.document.page_content}" for m in matches)
        response = self.chain.invoke({"context": context or "No matching excerpts.", "question": question})
        citations = [Citation(filename=str(m.document.metadata["filename"]), page=int(m.document.metadata["page"]), chunk_id=str(m.document.metadata["chunk_id"]), excerpt=m.document.page_content[:240]) for m in matches]
        return AnswerResponse(answer=str(response.content), citations=citations, request_id=str(uuid4()))
