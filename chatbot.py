import requests
import os 
from dotenv import load_dotenv

# 1. CRITICAL: You must call the function to actually load the variables
load_dotenv() 

# 2. Check your .env file; if it's written as API_KEY=..., use uppercase here
API_KEY = os.getenv("API_KEY") 
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def get_chat_response(user_message: str) -> str:
    """
    Sends a message to OpenRouter and returns the chatbot response as a string.
    """

    if not API_KEY:
        return "Error: API_KEY not found. Please check your .env file and variable name."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://agromarket-3.onrender.com", # Required by OpenRouter
        "X-Title": "College Chatbot"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo", 
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }

    try:
        # Send the request
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=20
        )
        
        # This will catch 4xx and 5xx errors
        response.raise_for_status()
        
        # Parse JSON and safely navigate the dictionary
        data = response.json()
        
        # Using .get() prevents the code from crashing if 'choices' is missing
        choices = data.get("choices", [])
        if choices:
            return choices[0].get("message", {}).get("content", "No content in message.")
        else:
            return f"Error: Unexpected API response structure: {data}"

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err} - {response.text}"
    except requests.RequestException as e:
        return f"Connection error: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

# --- Example Usage ---
# if __name__ == "__main__":
#     print(get_chat_response("Hello, what services do you provide?"))
