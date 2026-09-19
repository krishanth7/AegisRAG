"""Domain models."""
from pydantic import BaseModel, Field

class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str
    filename: str
    page: int = Field(ge=1)
    text: str = Field(min_length=1)
    content_sha256: str

class Citation(BaseModel):
    filename: str
    page: int = Field(ge=1)
    chunk_id: str
    excerpt: str

class QueryRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    top_k: int | None = Field(default=None, ge=1, le=20)

class AnswerResponse(BaseModel):
    answer: str
    citations: list[Citation]
    request_id: str
