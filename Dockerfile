FROM python:3.11-slim

WORKDIR /app

# Disable Python buffering for immediate log output
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-u", "bot.py"]
