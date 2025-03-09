# Unlimited OnDemand Auto Extender

Dieses Tool automatisiert das Nachbuchen von Datenvolumen bei SIM24- und 1&1-Unlimited-Demand-Tarifen. Bei diesen Tarifen muss nach Verbrauch der ersten 50GB das Datenvolumen manuell in Schritten nachgebucht werden. Dieser Prozess wird durch dieses Script vollautomatisch erledigt.

| Funktion | Beschreibung |
|----------|--------------|
| **Unterstützte Anbieter** | SIM24, 1&1 |
| **Automatisierung** | Nachbuchung von Datenvolumen, Überwachung des Verbrauchs |
| **Installation** | Docker (siehe [Installation & Einrichtung](#installation--einrichtung)) |
| **Anfänger-Guide** | [Für Docker-Anfänger](#für-anfänger--noch-nie-mit-docker-gearbeitet) |
| **Konfiguration** | Über Umgebungsvariablen (USERNAME, PASSWORD, SERVICE, etc.) |
| **Mehrere Tarife** | Unterstützung für mehrere 1&1-Tarife über TARIFF_ID |

## Features

- Automatische Anmeldung im SIM24- oder 1&1-Portal
- Kontinuierliche Überwachung des Datenvolumens
- Automatisches Nachbuchen bei Bedarf
- Ausführliche Logging-Funktionen
- Dockerisierte Lösung für einfache Installation
- Unterstützung für mehrere Tarife bei 1&1 (Auswahl eines spezifischen Tarifs möglich)

## Voraussetzungen

- Docker auf dem System installiert
- SIM24 oder 1&1 Account-Zugangsdaten
- Ein aktiver Unlimited-Demand-Tarif bei einem der unterstützten Anbieter

## Installation & Einrichtung

1. Image herunterladen:
```bash
docker pull ghcr.io/danielwte/unlimited-ondemand-auto-extender:latest
```

2. Container starten:
```bash
docker run -d \
  -e USERNAME="service-username" \
  -e PASSWORD="service-password" \
  -e SERVICE="service" \
  -e CHECK_INTERVAL=300 \
  --name unlimited-ondemand-auto-extender \
  ghcr.io/danielwte/unlimited-ondemand-auto-extender:latest
```

### Umgebungsvariablen

- `USERNAME`: Der Benutzername für das entsprechende Portal
- `PASSWORD`: Das Passwort für das entsprechende Portal
- `CHECK_INTERVAL`: Prüfintervall in Sekunden (Standard: 300)
- `SERVICE`: Der zu überwachende Service (Standard: sim24, Optionen: sim24, 1und1)
- `TARIFF_ID`: (Optional) Die ID eines spezifischen Tarifs bei 1&1, wenn mehrere Tarife vorhanden sind

### Mehrere Tarife bei 1&1

Wenn Sie mehrere Tarife in Ihrem 1&1-Konto haben, können Sie einen spezifischen Tarif für die automatische Nachbuchung auswählen:

1. Starten Sie den Container zunächst ohne TARIFF_ID, um alle verfügbaren Tarife zu sehen:
```bash
docker run -d \
  -e USERNAME="service-username" \
  -e PASSWORD="service-password" \
  -e SERVICE="1und1" \
  -e CHECK_INTERVAL=300 \
  --name unlimited-ondemand-auto-extender \
  ghcr.io/danielwte/unlimited-ondemand-auto-extender:latest
```

2. Prüfen Sie die Logs, um die Tarif-IDs zu sehen:
```bash
docker logs unlimited-ondemand-auto-extender
```

3. Starten Sie den Container neu mit der gewünschten TARIFF_ID:
```bash
docker stop unlimited-ondemand-auto-extender
docker rm unlimited-ondemand-auto-extender
docker run -d \
  -e USERNAME="service-username" \
  -e PASSWORD="service-password" \
  -e SERVICE="1und1" \
  -e CHECK_INTERVAL=300 \
  -e TARIFF_ID="IHRE_TARIF_ID" \
  --name unlimited-ondemand-auto-extender \
  ghcr.io/danielwte/unlimited-ondemand-auto-extender:latest
```

## Logs einsehen

Die Logs können wie folgt eingesehen werden:
```bash
docker logs unlimited-ondemand-auto-extender
```

## Container-Verwaltung

Container neustarten:
```bash
docker restart unlimited-ondemand-auto-extender
```

Container stoppen:
```bash
docker stop unlimited-ondemand-auto-extender
```

Container entfernen:
```bash
docker rm unlimited-ondemand-auto-extender
```

## Automatischer Start nach Systemneustart

Für einen automatischen Start nach einem Systemneustart:
```bash
docker run -d \
  --restart unless-stopped \
  -e USERNAME="service-username" \
  -e PASSWORD="service-password" \
  -e SERVICE="service" \
  -e CHECK_INTERVAL=300 \
  --name unlimited-ondemand-auto-extender \
  ghcr.io/danielwte/unlimited-ondemand-auto-extender:latest
```

## Sicherheit

- Die Zugangsdaten werden nur innerhalb des Containers verwendet
- Es werden keine Daten persistent gespeichert
- Die Kommunikation erfolgt direkt mit dem Portal des entsprechenden Anbieters

## Disclaimer

Dieses Tool ist ein inoffizielles Hilfsprogramm und steht in keiner Verbindung zu SIM24 oder 1&1. Die Nutzung erfolgt auf eigene Verantwortung.

## Für Anfänger / Noch nie mit Docker gearbeitet

Wenn du noch nie mit Docker gearbeitet hast, findest du hier eine einfache Anleitung, um loszulegen:

| Betriebssystem | Schritt-für-Schritt-Anleitung |
|----------------|-------------------------------|
| **Windows**    | 1. **Docker Desktop installieren**: <br> - Lade [Docker Desktop für Windows](https://www.docker.com/products/docker-desktop) herunter <br> - Führe die Installationsdatei aus und folge den Anweisungen <br> - Starte deinen Computer neu nach der Installation <br> 2. **Docker starten**: <br> - Starte Docker Desktop über das Startmenü <br> - Warte, bis das Docker-Symbol in der Taskleiste grün wird (Docker läuft dann) <br> 3. **PowerShell oder Eingabeaufforderung öffnen**: <br> - Drücke `Win + X` und wähle "Windows PowerShell" oder "Eingabeaufforderung" <br> 4. **Tool starten**: <br> - Kopiere den Befehl aus dem Abschnitt "Installation & Einrichtung" und füge ihn in die PowerShell ein <br> - Ersetze die Platzhalter mit deinen tatsächlichen Zugangsdaten |
| **Linux**      | 1. **Docker installieren**: <br> - Öffne ein Terminal mit `Strg + Alt + T` <br> - Führe folgende Befehle aus: <br> ```sudo apt update``` <br> ```sudo apt install docker.io``` <br> ```sudo systemctl enable --now docker``` <br> 2. **Benutzer zur Docker-Gruppe hinzufügen**: <br> ```sudo usermod -aG docker $USER``` <br> - Melde dich ab und wieder an, damit die Änderungen wirksam werden <br> 3. **Tool starten**: <br> - Kopiere den Befehl aus dem Abschnitt "Installation & Einrichtung" und füge ihn ins Terminal ein <br> - Ersetze die Platzhalter mit deinen tatsächlichen Zugangsdaten |
| **macOS**      | 1. **Docker Desktop installieren**: <br> - Lade [Docker Desktop für Mac](https://www.docker.com/products/docker-desktop) herunter <br> - Öffne die heruntergeladene .dmg-Datei und ziehe Docker in deinen Applications-Ordner <br> - Starte Docker aus dem Applications-Ordner <br> - Erlaube die Installation, wenn du dazu aufgefordert wirst <br> 2. **Docker starten**: <br> - Warte, bis das Docker-Symbol in der Menüleiste erscheint und nicht mehr animiert ist <br> 3. **Terminal öffnen**: <br> - Öffne das Terminal über Spotlight (Cmd + Leertaste) und tippe "Terminal" <br> 4. **Tool starten**: <br> - Kopiere den Befehl aus dem Abschnitt "Installation & Einrichtung" und füge ihn ins Terminal ein <br> - Ersetze die Platzhalter mit deinen tatsächlichen Zugangsdaten |

### Was ist Docker?

Docker ist eine Plattform, die es ermöglicht, Anwendungen in sogenannten "Containern" auszuführen. Ein Container ist wie ein kleiner, isolierter Computer innerhalb deines Computers, der alles enthält, was die Anwendung zum Laufen braucht. Du musst dich nicht um die Installation von Abhängigkeiten oder Konfigurationen kümmern - alles ist bereits im Container enthalten.

### Wichtige Docker-Befehle für Anfänger

- `docker pull [IMAGE]`: Lädt ein Docker-Image herunter
- `docker run [OPTIONS] [IMAGE]`: Startet einen Container
- `docker ps`: Zeigt laufende Container an
- `docker logs [CONTAINER]`: Zeigt die Logs eines Containers an
- `docker stop [CONTAINER]`: Stoppt einen laufenden Container
- `docker restart [CONTAINER]`: Startet einen Container neu

### Konkretes Beispiel: SIM24 Auto-Extender einrichten

Hier ist ein konkretes Beispiel, wie du den Unlimited OnDemand Auto Extender für einen SIM24-Tarif einrichtest:

1. **Docker installieren** (siehe Tabelle oben)

2. **Terminal/PowerShell öffnen** (je nach Betriebssystem)

3. **Docker-Image herunterladen**:
   ```bash
   docker pull ghcr.io/danielwte/unlimited-ondemand-auto-extender:latest
   ```

4. **Container starten** (ersetze die Platzhalter mit deinen echten Daten):
   ```bash
   docker run -d \
     -e USERNAME="deine-sim24-email" \
     -e PASSWORD="dein-sim24-passwort" \
     -e SERVICE="sim24" \
     -e CHECK_INTERVAL=300 \
     --name unlimited-ondemand-auto-extender \
     --restart unless-stopped \
     ghcr.io/danielwte/unlimited-ondemand-auto-extender:latest
   ```

5. **Überprüfen, ob der Container läuft**:
   ```bash
   docker ps
   ```
   Du solltest deinen Container in der Liste sehen.

6. **Logs überprüfen**:
   ```bash
   docker logs unlimited-ondemand-auto-extender
   ```
   In den Logs siehst du, ob die Anmeldung erfolgreich war und wie viel Datenvolumen noch verfügbar ist.

Das war's! Der Container läuft jetzt im Hintergrund und kümmert sich automatisch um das Nachbuchen von Datenvolumen, wenn nötig.

### Häufige Probleme für Anfänger

| Problem | Lösung |
|---------|--------|
| **"Permission denied" bei Docker-Befehlen (Linux)** | Führe die Befehle mit `sudo` aus oder stelle sicher, dass dein Benutzer zur Docker-Gruppe hinzugefügt wurde: <br> ```sudo usermod -aG docker $USER``` <br> Danach abmelden und wieder anmelden. |
| **Docker startet nicht (Windows)** | 1. Stelle sicher, dass Virtualisierung im BIOS aktiviert ist <br> 2. Überprüfe, ob WSL 2 installiert ist: ```wsl --status``` <br> 3. Falls nicht, installiere es: ```wsl --install``` |
| **Docker startet nicht (macOS)** | 1. Starte deinen Mac neu <br> 2. Stelle sicher, dass du genügend freien Speicherplatz hast <br> 3. Überprüfe, ob Docker Desktop die erforderlichen Berechtigungen hat |
| **Container startet, aber funktioniert nicht** | Überprüfe die Logs mit: ```docker logs unlimited-ondemand-auto-extender``` <br> Häufige Ursachen: <br> - Falsche Zugangsdaten <br> - Falscher Service-Name (muss genau "sim24" oder "1und1" sein) |
| **"Image not found" Fehler** | Stelle sicher, dass du den Image-Namen korrekt eingegeben hast: <br> ```ghcr.io/danielwte/unlimited-ondemand-auto-extender:latest``` |
| **Container läuft, aber bucht nicht nach** | 1. Überprüfe die Logs auf Fehlermeldungen <br> 2. Stelle sicher, dass dein Tarif unterstützt wird <br> 3. Überprüfe, ob die Webseite des Anbieters erreichbar ist |