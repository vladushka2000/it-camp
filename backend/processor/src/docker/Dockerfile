FROM python:3.11-slim

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /app
COPY ./src/poetry.lock ./src/pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY ./src/ ./

EXPOSE 7773

CMD ["python3", "-u", "main.py"]
