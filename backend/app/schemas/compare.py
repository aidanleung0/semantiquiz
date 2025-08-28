from pydantic import BaseModel
from typing import Optional

class CompareRequest(BaseModel):
    word: str
    ground_truth: str
    user_input: str

class CompareResponse(BaseModel):
    job_id: str
