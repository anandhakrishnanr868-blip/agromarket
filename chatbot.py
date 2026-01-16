# chatbot.py
from pydantic import BaseModel
import requests

API_KEY = "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"  
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

class CodeInput(BaseModel):
    msg: str

def get_chat_response(message: str) -> str:
    """
    Sends a message to OpenRouter chat API and returns the model response.
    Handles Unicode properly to avoid ASCII encoding errors.
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",  # Use a valid OpenRouter model
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ],
        "temperature": 0.7
    }

    try:
        res = requests.post(OPENROUTER_URL, json=payload, headers=headers, timeout=20)
        res.raise_for_status()
        res.encoding = 'utf-8'  # Force UTF-8 decoding
    except requests.RequestException as e:
        return f"Error: Request failed — {str(e)}"

    try:
        data = res.json()
        # Ensure the content is a proper string
        content = data["choices"][0]["message"]["content"]
        return str(content)  # Keep as Unicode string
    except (KeyError, ValueError):
        return f"Error: Invalid JSON returned — {res.text}"

