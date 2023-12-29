FROM python:3.10-slim

RUN apt-get update -qq \
 && apt-get install -y --no-install-recommends \
    build-essential \
	cmake \
    gcc \
    libpq-dev \
    curl \
 && apt-get autoremove -y

WORKDIR /app

RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --no-cache-dir -U 'pip<20' && \
	pip install --upgrade pip && \
    pip install rasa spacy && \
    python -m spacy download de_core_news_lg && \
    python -m spacy link de_core_news_lg de
	
COPY . /app

RUN . /opt/venv/bin/activate && \
	rasa train

EXPOSE 5005