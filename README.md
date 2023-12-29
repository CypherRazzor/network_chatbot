# networkbot_chat

## Nutzung Python virtuelle Umgebung

Python Version auf dem PC abfragen
```bash
py -0
```

Einrichten einer virtuellen Umgebung
```bash
py -3.10 -m venv env
.\env\Scripts\Activate.ps1
```

Aktualisieren von pip und Installieren von Rasa und Abhängigkeiten

```bash
python.exe -m pip install --upgrade pip  # Upgrade pip
pip3 install rasa
pip3 install rasa[spacy]
pip3 install rasa[full]
python -m spacy download de_core_news_lg
```
Falls ein neue Projekt gestartet werden soll.

```bash
rasa init
```
Nutzung für Rasa Run und Rasa Actions mit 2 Powershell Instanzen

1. In der ersten PowerShell-Instanz starten Sie Rasa mit dem Befehl:
   ```bash
   rasa train
   rasa run
   ```
2. In der zweiten PowerShell-Instanz starten Sie Rasa Actions mit dem Befehl:
   ```bash
   rasa run actions
   ```

## Nutzung von Docker
Alle Dockerfiles und docker-compose.yml sind korrekt platziert.
```bash
cd %Projektordner%
docker compose build # zum Bauen der Docker Container
docker compose up # Starten Dockercontainer
docker compose down # Beenden aller Dockercontainer
```
Verwendung des erstellten PS Skriptes

1. Ordner im Explorer öffnen
2. Rechtsklick auf das Skript start_and_stop_chatbot.ps1
3. Klick auf "Mit Powershell ausführen"

## Tests mit Python

In Projektordner wechseln mit 

```bash
cd %Projektordner%
```

Installiere die Anforderungen

```bash
pip install -r .\tests\requirements.txt
```

Starten von den verschiedenen Testdateien
```bash
python .\tests\tests_actions.py
python .\tests\test_calculateSubnet.py
python .\tests\test_docker_automated_action_server.py
```
