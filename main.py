import requests
import os
import requests
from dotenv import load_dotenv
from chromadb_handler import retrieve_context

# Load environment variables
load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    raise ValueError("DEEPSEEK_API_KEY is not set in the environment variables.")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

def generate_response(user_query):
    # Retrieve relevant context
    context = retrieve_context(user_query)
    
    # Craft the prompt
    system_prompt = f"""
    Answer the user's question based ONLY on this context:
    {context}
    If unsure, say 'I don't know.'
    """
    
    # Call DeepSeek
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}"}
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]
    }
    response = requests.post(DEEPSEEK_URL, json=payload, headers=headers)
    
    # Print the full response for debugging
    print("Response Status Code:", response.status_code)
    print("Response JSON:", response.json())
    
    # Safely access the response content
    try:
        return response.json()["choices"][0]["message"]["content"]
    except KeyError:
        return "Unexpected response format from the API."



# Test
response = generate_response("Can I get a refund after 2 weeks?")
print(response)  # Output: "Yes, our return policy allows refunds within 30 days."