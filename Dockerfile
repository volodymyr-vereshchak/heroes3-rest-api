# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /app

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p /vol/cinema_service/media/

RUN adduser --disabled-password --no-create-home hero-user

RUN chown -R hero-user:hero-user /vol/
RUN chmod -R 755 /vol/heroes3_api/


USER hero-user