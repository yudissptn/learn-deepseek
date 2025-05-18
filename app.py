import twilio
import os
from flask import Flask, request, jsonify, session
from rag_deepseek import generate_response  # Your RAG-DeepSeek function

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook(): # Twilio sends data as form-data, not JSON
    incoming_msg = request.form.get("Body", "").strip()  # User's message
    user_id = request.form.get("From")        # User's WhatsApp number

    # Initialize user-specific chat history
    if f"chat_history_{user_id}" not in session:
        session[f"chat_history_{user_id}"] = []

    # Add latest message to history (limit to last 3 messages)
    session[f"chat_history_{user_id}"].append(incoming_msg)
    session[f"chat_history_{user_id}"] = session[f"chat_history_{user_id}"][-3:]  # Keep last 3
    
    # Generate context from memory + RAG
    context = "\n".join(session[f"chat_history_{user_id}"])
    prompt = f"Chat history:\n{context}\n\nUser: {incoming_msg}"
    
    # Generate your RAG + DeepSeek response
    bot_response = generate_response(prompt)  # Your function

    # Store bot's reply in history (optional)
    session[f"chat_history_{user_id}"].append(bot_response)
    
    # Twilio expects TwiML (XML) or plain text as a response
    from twilio.twiml.messaging_response import MessagingResponse
    twiml = MessagingResponse()
    twiml.message(bot_response)
    
    return str(twiml)  # Return TwiML to Twilio

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Use Render's $PORT or default to 8080
    app.run(host="0.0.0.0", port=port)  # Critical for Render compatibility