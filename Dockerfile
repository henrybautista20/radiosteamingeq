FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive TZ=America/Guayaquil

RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg ca-certificates tzdata && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python", "main.py"]
