FROM python:3.6.4

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

