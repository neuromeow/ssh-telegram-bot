FROM python:3.8-slim

WORKDIR /ssh-telegram-bot

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY bot /ssh-telegram-bot/bot

CMD ["python", "-m", "bot"]
