FROM python:3.11

RUN pip install poetry==1.2.0

WORKDIR /app

COPY pyproject.toml poetry.lock manage.py ./

RUN poetry install

COPY narvi/ ./narvi/
COPY words/ ./words/
COPY tests/ ./tests/
