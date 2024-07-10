FROM public.ecr.aws/lambda/python:3.10 as base

RUN pip install "poetry~=1.5.0"

COPY poetry.lock pyproject.toml README.md ./
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root --only main


# -----------------------------
FROM base as test

RUN poetry install --no-interaction --no-ansi --no-root

COPY src src
COPY tests tests

ENV DYNAMODB_TABLE_NAME=example_table
RUN python -m unittest


# -----------------------------
FROM base as build

COPY src .
RUN chmod 644 $(find . -type f)
RUN chmod 755 $(find . -type d)