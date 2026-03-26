import requests
import os 
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv() 

# Ensure your .env file has: API_KEY=sk-or-v1-your-key-here
API_KEY = os.getenv("API_KEY") 
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def get_chat_response(user_message: str) -> str:
    if not API_KEY:
        return "Error: API_KEY not found. Please check your .env file."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://agromarket-3.onrender.com",
        "X-Title": "AgroMarket Assistant"
    }

    payload = {
        # Updated to the free model from your screenshot
        "model": "openai/gpt-oss-120b:free", 
        "messages": [
            {
                "role": "system", 
                "content": (
                    "You are a specialized Agriculture Assistant. "
                    "Your expertise is strictly limited to: "
                    "1. Agriculture techniques and crop management. "
                    "2. Government agriculture schemes and subsidies. "
                    "3. Current crop market rates and trends. "
                    "If the user asks about anything outside these three areas, "
                    "you must politely decline and state that you only handle agriculture-related queries."
                )
            },
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.4 
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=30 # Increased timeout for larger models
        )
        response.raise_for_status()
        
        data = response.json()
        choices = data.get("choices", [])
        
        if choices:
            return choices[0].get("message", {}).get("content", "No content found.")
        else:
            return f"Error: The model returned an empty response. {data}"

    except requests.exceptions.HTTPError as http_err:
        # This will help debug that 401 'User Not Found' error
        return f"Access Error: {http_err} - Check if your API Key is correct."
    except Exception as e:
        return f"Error: {str(e)}"

# --- Test ---
# print(get_chat_response("What are the current market rates for wheat?"))
