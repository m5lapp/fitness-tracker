FROM docker.io/python:3.11

ENV ALLOWED_HOSTS "127.0.0.1,localhost"
ENV DEBUG 0
ENV PYTHONUNBUFFERED 1

WORKDIR /app/

USER 1000

COPY requirements.txt ./
RUN apt update && \
    apt upgrade -y && \
    pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:8080", "fitnesstracker.wsgi"]
