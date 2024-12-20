import json
import openai
from fastapi import HTTPException
from app.core.config import settings
from app.core.openai_utils import call_openai_api

openai.api_key = settings.OPENAI_API_KEY

def analyze_review(review_text: str) -> dict:
    """
    Analyzes the review to determine if it is spam and classifies its sentiment.
    Returns:
        dict: Contains 'isSpam' (boolean) and 'sentiment' (string).
    """
    prompt = (
        f"Analyze the following review:\n\n"
        f"Review: {review_text}\n\n"
        f"Return the result as a JSON object with two keys:\n"
        f"1. 'isSpam': A boolean indicating if the review is spam (true or false).\n"
        f"2. 'sentiment': A string representing the sentiment category "
        f"(Very negative, Negative, Neutral, Positive, Very positive).\n\n"
        f"Example output:\n"
        f"{{\"isSpam\": false, \"sentiment\": \"Positive\"}}\n\n"
        f"Now analyze the review."
    )
    try:
        response = call_openai_api(prompt, max_tokens=50, temperature=0)
        return json.loads(response)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse the response as JSON.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred: {str(e)}")

def summarize_reviews(reviews: list[str]) -> dict:
    """
    Summarizes the provided reviews to highlight strengths, weaknesses, and general sentiment.
    Args:
        reviews (list[str]): A list of review texts.
    Returns:
        dict: A summary of the key points.
    """
    combined_reviews = "\n".join(reviews)
    prompt = (
        f"Analyze the following product reviews:\n\n"
        f"{combined_reviews}\n\n"
        f"Provide a summary with the following points:\n"
        f"1. General sentiment (Positive, Neutral, Negative).\n"
        f"2. Strengths or what people liked about the product.\n"
        f"3. Weaknesses or areas for improvement.\n"
        f"4. Any notable recurring themes or patterns in the reviews.\n\n"
        f"Output format:\n"
        f"{{\n"
        f"  \"generalSentiment\": \"Positive\",\n"
        f"  \"strengths\": [\"Easy to use\", \"Great support\"],\n"
        f"  \"weaknesses\": [\"High price\", \"Limited features\"],\n"
        f"  \"themes\": [\"Excellent battery life\", \"Too bulky\"]\n"
        f"}}"
    )
    try:
        response = call_openai_api(prompt, max_tokens=300, temperature=0.5)
        return json.loads(response)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse the response as JSON.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred: {str(e)}")

def professionalize_review(review_text: str) -> str:
    """
    Professionalizes the given review text, making it more formal and polished.
    Args:
        review_text (str): The original review text.
    Returns:
        str: The professionalized review.
    """
    prompt = (
        f"Rewrite the following review to make it more formal and polished while retaining its original meaning:\n\n"
        f"Original Review: {review_text}\n\n"
        f"Professionalized Review:"
    )
    try:
        return call_openai_api(prompt, max_tokens=150, temperature=0.5)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred: {str(e)}")
