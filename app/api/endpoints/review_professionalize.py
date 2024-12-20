from fastapi import APIRouter, HTTPException
from app.core.openai_client import professionalize_review
from app.models.validation_models import ProfessionalizeRequest

router = APIRouter()

@router.post("/professionalize")
async def professionalize_review_endpoint(request: ProfessionalizeRequest):
    """
    Endpoint to professionalize a review text.
    """
    try:
        professionalized_text = professionalize_review(request.reviewText)
        return {"originalText": request.reviewText, "professionalizedText": professionalized_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
