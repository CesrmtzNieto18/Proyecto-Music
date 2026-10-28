FROM python:3.10-slim

# Instalamos LilyPond, Timidity (para el audio) y dependencias
RUN apt-get update && apt-get install -y \
    lilypond \
    timidity \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD gunicorn --bind 0.0.0.0:$PORT app:app