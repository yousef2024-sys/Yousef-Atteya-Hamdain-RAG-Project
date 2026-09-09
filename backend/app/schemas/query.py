from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)
    top_k: int = Field(default=3, ge=1, le=5)


class Citation(BaseModel):
    id: str
    title: str
    section: str
    excerpt: str
    score: float
    document_type: str


class RetrievalMeta(BaseModel):
    query: str
    chunks_considered: int
    latency_ms: int
    model: str
    grounded: bool


class QueryResponse(BaseModel):
    answer: str
    sources: list[Citation]
    related_questions: list[str]
    retrieval: RetrievalMeta