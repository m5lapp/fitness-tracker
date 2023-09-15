FROM docker.io/python:3.11-alpine3.18

ENV ALLOWED_HOSTS "127.0.0.1,localhost"
ENV DEBUG 0
ENV PYTHONUNBUFFERED 1

WORKDIR /app/

USER 1000

COPY requirements.txt ./

RUN apk update && \
    apk add postgresql-libs && \
    apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8080

CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:8080", "fitnesstracker.wsgi"]
