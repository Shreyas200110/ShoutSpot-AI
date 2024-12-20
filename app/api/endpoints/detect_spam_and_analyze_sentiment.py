from fastapi import APIRouter, HTTPException
from app.core.openai_client import analyze_review
from app.models.validation_models import ReviewRequest

router = APIRouter()

@router.post("/detect_spam_sentiment")
async def detect_spam_and_analyze_sentiment(review: ReviewRequest):
    """
    Endpoint to detect spam and analyze sentiment for a review text.
    Combines both functionalities in a single OpenAI call.
    """
    try:
        analysis = analyze_review(review.reviewText)
        return {
            "reviewText": review.reviewText,
            "isSpam": analysis["isSpam"],
            "sentiment": analysis["sentiment"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
