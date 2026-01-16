import requests


API_KEY = "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"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def get_chat_response(user_message: str) -> str:
    """
    Sends a message to OpenRouter and returns the chatbot response as string.
    """

    if not API_KEY:
        return "Error: API_KEY not found. Please set it in .env file."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://agromarket-3.onrender.com",
        "X-Title": "College Chatbot"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=20
        )
        response.raise_for_status()
    except requests.RequestException as e:
        return f"Error: Request failed — {str(e)}"

    try:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception:
        return f"Error: Invalid response format — {response.text}"
