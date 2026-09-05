from pydantic import BaseModel
from typing import Optional, List

class ChatResponse(BaseModel):
    answer: str
    sources: List[dict] = []