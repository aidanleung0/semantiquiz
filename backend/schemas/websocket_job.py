from pydantic import BaseModel
from typing import Optional

class WebsocketResponse(BaseModel):
    job_id: str
    word: str
    user_input: str
    ground_truth: str
    feedback:str
    example: str
