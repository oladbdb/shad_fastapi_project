FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src /app/src

ENV APP_HOST=0.0.0.0 \
    APP_PORT=8000

CMD ["sh", "-c", "uvicorn src.main:app --host ${APP_HOST:-0.0.0.0} --port ${APP_PORT:-8000}"]
