FROM python:3.12-slim-buster

WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt .
RUN apt-get update && apt-get install -y wget \
    && wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.6.1.tar.gz \
    && rm dockerize-linux-amd64-v0.6.1.tar.gz \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8000

# Use dockerize to wait for dependencies (PostgreSQL, Redis, etc.)
CMD ["dockerize", "-wait", "tcp://postgres_service:5436", "-timeout", "1m", "--", "python", "main.py"]