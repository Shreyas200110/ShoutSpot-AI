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
    Summarizes the provided reviews to highlight strengths, weaknesses, and general sentiment in sentences.
    Args:
        reviews (list[str]): A list of review texts.
    Returns:
        dict: A summary of the key points with sentence-based descriptions.
    """
    combined_reviews = "\n".join(reviews)
    prompt = (
        f"Analyze the following product reviews:\n\n"
        f"{combined_reviews}\n\n"
        f"Provide a detailed summary with the following points:\n"
        f"1. General sentiment: Provide a description of the overall sentiment in multiple sentences.\n"
        f"2. Strengths: List the key strengths of the product, described in full sentences.\n"
        f"3. Weaknesses: Highlight any weaknesses or areas for improvement, described in full sentences.\n"
        f"4. Recurring themes: Identify recurring themes or patterns across the reviews, described in full sentences.\n\n"
        f"Output format:\n"
        f"{{\n"
        f"  \"sentiment\": [\"Overall, the reviews are positive, emphasizing satisfaction with the product's quality and usability.\", ...],\n"
        f"  \"strengths\": [\"The product is user-friendly and easy to navigate.\", \"Customer support is responsive and helpful.\", ...],\n"
        f"  \"weaknesses\": [\"The price is relatively high compared to competitors.\", \"Some features are missing or limited.\", ...],\n"
        f"  \"themes\": [\"Many users praised the excellent battery life.\", \"Several users found the product too bulky for everyday use.\", ...]\n"
        f"}}"
        f"In the arrays you can add multiple points in form of sentences, think as you are helping an organization to improve their product with this summary"
    )

    try:
        response = call_openai_api(prompt, max_tokens=500, temperature=0.7)
        return {"summary": json.loads(response)}
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
        f"Provide the output in the following JSON format:\n"
        f"{{\n"
        f"  \"professionalizedText\": \"Your professionalized review here.\"\n"
        f"}}"
    )

    try:
        response =  call_openai_api(prompt, max_tokens=150, temperature=0.5)
        return json.loads(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred: {str(e)}")
