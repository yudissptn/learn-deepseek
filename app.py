import twilio
import os
from flask import Flask, request, jsonify
from rag_deepseek import generate_response  # Your RAG-DeepSeek function

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook(): # Twilio sends data as form-data, not JSON
    incoming_msg = request.form.get("Body", "").strip()  # User's message
    sender_number = request.form.get("From", "")        # User's WhatsApp number
    
    # Generate your RAG + DeepSeek response
    bot_response = generate_response(incoming_msg)  # Your function
    
    # Twilio expects TwiML (XML) or plain text as a response
    from twilio.twiml.messaging_response import MessagingResponse
    twiml = MessagingResponse()
    twiml.message(bot_response)
    
    return str(twiml)  # Return TwiML to Twilio

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Use Render's $PORT or default to 8080
    app.run(host="0.0.0.0", port=port)  # Critical for Render compatibility