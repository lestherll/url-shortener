# syntax = docker/dockerfile:1.4

FROM tiangolo/uvicorn-gunicorn:python3.11 AS builder

WORKDIR /app

COPY requirements.txt .
COPY requirements-dev.txt .

RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

COPY . .

CMD ["uvicorn", "url_shortener.main:app", "--host", "0.0.0.0", "--port", "8000"]
