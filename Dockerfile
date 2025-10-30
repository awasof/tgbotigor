FROM python:3.11-slim

WORKDIR /app

# Disable Python buffering for immediate log output
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Temporarily use simple bot for debugging
CMD ["python", "-u", "bot_simple.py"]
