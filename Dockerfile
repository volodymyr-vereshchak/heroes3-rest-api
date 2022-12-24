# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /app

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p /download/img/full/

RUN adduser --disabled-password --no-create-home hero-user

RUN chown -R hero-user:hero-user /download/

RUN chmod -R 755 /download/

USER hero-user
