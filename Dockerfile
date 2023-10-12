# syntax=docker/dockerfile:1

FROM python:3.10-alpine

WORKDIR /app
RUN apk update && apk add postgresql gcc musl-dev python3-dev libffi-dev libpq-dev

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev


#COPY schema.json schema.json
COPY src src

ENV PYTHONPATH="${PYTHONPATH}:/app"
CMD ["python3", "src/main.py"]
