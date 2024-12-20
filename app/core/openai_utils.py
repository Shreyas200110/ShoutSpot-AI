from fastapi import HTTPException
from openai import OpenAI
from app.core.config import settings

DEFAULT_MODEL = settings.MODEL_ENGINE  # Default model, e.g., "gpt-4"

def call_openai_api(prompt: str, max_tokens: int, temperature: float = 0.5, model: str = None) -> str:
    """
    Calls the OpenAI ChatCompletion API with the given prompt and parameters.
    Args:
        prompt (str): The prompt for the model.
        max_tokens (int): Maximum tokens to generate.
        temperature (float): Controls randomness of the output.
        model (str): The model to use (overrides default if provided).
    Returns:
        str: The generated response content.
    """
    model_to_use = settings.MODEL_ENGINE
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    try:
        response = client.chat.completions.create(
            model=model_to_use,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred: {str(e)}")
