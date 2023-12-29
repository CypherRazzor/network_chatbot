FROM python:3.10-slim

RUN apt-get update -qq \
 && apt-get install -y --no-install-recommends \
    build-essential \
	cmake \
    gcc \
    libpq-dev \
    curl \
 && apt-get autoremove -y

# Setzen Sie das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopieren Sie die Anwendungsdateien in den Container
COPY ./actions /app



# Installieren Sie notwendige Python-Pakete
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --no-cache-dir -U 'pip<20' && \
	pip install --upgrade pip && \
    pip install python-dotenv rasa requests

# Legen Sie den Port fest, auf dem der Container lauschen soll
EXPOSE 5055

# Definieren Sie den Standardbefehl zum Ausführen des Containers
#CMD ["python", "rasa", "run", "actions", "--debug"]
