FROM python:3.12-alpine
LABEL authors="zwickvitaly"

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY app/ .

ENTRYPOINT uvicorn main:app --host 0.0.0.0 --port 8080


