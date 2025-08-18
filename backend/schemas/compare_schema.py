from pydantic import BaseModel

class CompareRequest(BaseModel):
    ground_truth: str
    user_input: str

class CompareResponse(BaseModel):
    ground_truth: str
    user_input: str
    similarity: float