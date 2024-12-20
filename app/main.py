from fastapi import FastAPI
from app.api.endpoints import detect_spam_and_analyze_sentiment, review_professionalize, reviews_summary
app = FastAPI(title="ShoutSpot AI", version="1.0.0")

# Include Routers
app.include_router(detect_spam_and_analyze_sentiment.router, prefix="", tags=["Text Generation"])
app.include_router(reviews_summary.router, prefix="", tags=["Review Summary"])
app.include_router(review_professionalize.router, prefix="", tags=["Review Professionalize"])

@app.get("/")
async def root():
    return {"message": "ShoutSpot AI welcomes you!!"}
