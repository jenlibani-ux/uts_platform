# Dockerfile — Flask Buku Tamu Digital (Tahap 5)
FROM python:3.11-slim

LABEL maintainer="Jenli Melinda Banik <jenlibani@gmail.com>" \
      description="Buku Tamu Digital — UTS Teknologi Platform"

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .
RUN mkdir -p /app/logs

EXPOSE 8000

CMD ["python", "app.py"]
