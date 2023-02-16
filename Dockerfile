FROM python:3.9 as base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

RUN rm -f tmp.db db.sqlite3

RUN rm -r accounts/migrations

RUN rm -r accounts_profile/migrations

RUN rm -r incident/migrations

RUN rm -r notifications/migrations

RUN rm -r role/migrations

RUN rm -r subscription/migrations

RUN python manage.py makemigrations accounts

RUN python manage.py makemigrations accounts_profile

RUN python manage.py makemigrations incident

RUN python manage.py makemigrations notifications

RUN python manage.py makemigrations role

RUN python manage.py makemigrations subscription

RUN python manage.py migrate

COPY . /app
