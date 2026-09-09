from fastapi import APIRouter, Request

from app.schemas.query import QueryRequest, QueryResponse

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/query", response_model=QueryResponse)
def query(payload: QueryRequest, request: Request) -> QueryResponse:
    result = request.app.state.retriever.answer(payload.question, payload.top_k)
    return QueryResponse.model_validate(result)