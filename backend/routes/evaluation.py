from fastapi import APIRouter
from schemas.compare import CompareRequest, CompareResponse
from services.evaluator import evaluate_definition

router = APIRouter()

@router.post("/compare-definition", response_model=CompareResponse)
async def compare_definition(payload: CompareRequest):
    return evaluate_definition(payload)
