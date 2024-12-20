from typing import List
from pydantic import BaseModel

class TextRequest(BaseModel):
    prompt: str
    max_tokens: int = 100

class ReviewRequest(BaseModel):
    reviewText: str

class ReviewsSummarizerRequest(BaseModel):
    reviews: List[str]

class ProfessionalizeRequest(BaseModel):
    reviewText: str