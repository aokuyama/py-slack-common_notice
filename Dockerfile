FROM python:3.7-alpine

ENV PYTHONIOENCODING utf-8
WORKDIR /app

RUN apk add --update

RUN pip install --upgrade pip && pip install requests
