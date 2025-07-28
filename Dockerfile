FROM python:3.11-slim

# Set up working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot code
COPY bot.py .
# COPY .env .

# Create logs directory
RUN mkdir -p logs

# Run the bot
CMD ["python", "bot.py"]
