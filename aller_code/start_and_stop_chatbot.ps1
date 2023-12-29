<#
Voraussetzungen für dieses Skript:
- Docker Desktop muss auf dem Windows-System installiert sein.
- Docker Desktop sollte so konfiguriert sein, dass es beim Start von Windows automatisch gestartet wird oder manuell gestartet werden muss, bevor dieses Skript ausgeführt wird.
- Dieses Skript muss im selben Verzeichnis wie Ihre `docker-compose.yml`-Datei abgelegt werden.
- Der Pfad zur lokalen HTML-Datei `chatroom.html` muss relativ zum Speicherort des Skripts korrekt sein.
- PowerShell muss mit ausreichenden Berechtigungen ausgeführt werden, um Docker-Befehle auszuführen und Webbrowser zu öffnen.
#>

# Pfad zur lokalen HTML-Datei, die geöffnet werden soll
$htmlFilePath = ".\html\chatroom.html"

# Überprüfen und Starten von Docker, falls nicht aktiv
$dockerRunning = $false
do {
    try {
        docker info > $null
        $dockerRunning = $true
    } catch {
        Write-Host "Docker läuft nicht. Bitte starten Sie die Docker Desktop Anwendung."
    }
    if (-not $dockerRunning) {
        Start-Sleep -Seconds 30
    }
} while (-not $dockerRunning)

# Überprüfen, ob der spezifische Container 'networkbot_chat-rasa' läuft
$specificContainerRunning = docker ps -f "name=networkbot_chat-rasa" -q
if ($specificContainerRunning) {
    Write-Host "Der Container 'networkbot_chat-rasa' läuft bereits. Er wird jetzt gestoppt."
    docker-compose down
    exit
}

# Docker Compose Build ausführen
docker-compose build

# Öffnen Sie die lokale HTML-Datei im Standardwebbrowser
Start-Process (Resolve-Path $htmlFilePath)

# F�ngt das Beenden des Skripts ab und f�hrt `docker-compose down` aus
trap {
    Write-Host "Das PowerShell-Fenster wird geschlossen. Docker Compose wird heruntergefahren..."
    docker-compose down
    exit
}

# Docker Compose Up ausf�hren
docker-compose up