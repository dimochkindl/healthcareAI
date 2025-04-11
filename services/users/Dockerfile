FROM python:3.11-slim-bullseye

WORKDIR /app


RUN apt-get update && apt-get install -y wget \
    && wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.6.1.tar.gz \
    && rm dockerize-linux-amd64-v0.6.1.tar.gz \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

## Add /app to Python path
#ENV PYTHONPATH=/app

EXPOSE 8005

CMD ["dockerize", "-wait", "tcp://postgres_service:5437", "-timeout", "1m", "--", "python", "/app/main.py"]