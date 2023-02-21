FROM python:3.9 as base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

# RUN rm -f tmp.db db.sqlite3

COPY . /app
