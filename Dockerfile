# Dockerfile

FROM python:3.9.2

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.1.5

WORKDIR /code

# requirements
COPY poetry.lock pyproject.toml /code/

# Create environment
RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false && poetry install
RUN pip install nox
RUN pip install nox_poetry

COPY . /code
