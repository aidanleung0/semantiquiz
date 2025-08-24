from pydantic import BaseModel
from typing import Optional

class CompareRequest(BaseModel):
    word: str
    ground_truth: str
    user_input: str

class CompareResponse(BaseModel):
    word: str
    similarity: str
    explanation: Optional[str] = None