# Use lightweight Python image
FROM python:3.9-slim

WORKDIR /app

# Install dependencies first (cached unless requirements.txt changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Set environment variables (Twilio/DeepSeek keys)
ENV DEEPSEEK_API_KEY=your_key_here
ENV TWILIO_ACCOUNT_SID=your_sid
ENV TWILIO_AUTH_TOKEN=your_token

# Run the app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "2", "app:app"]