from fastapi import APIRouter, HTTPException
from typing import List
from app.core.openai_client import summarize_reviews
from app.models.validation_models import ReviewsSummarizerRequest

router = APIRouter()

@router.post("/summarize")
async def summarize_reviews_endpoint(request: ReviewsSummarizerRequest):
    """
    Summarizes multiple reviews to provide insights about general sentiment, strengths, weaknesses, and patterns.
    """
    try:
        summary = summarize_reviews(request.reviews)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
