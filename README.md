# Unlimited OnDemand Auto Extender

Dieses Tool automatisiert das Nachbuchen von Datenvolumen bei SIM24- und 1&1-Unlimited-Demand-Tarifen. Bei diesen Tarifen muss nach Verbrauch der ersten 50GB das Datenvolumen manuell in Schritten nachgebucht werden. Dieser Prozess wird durch dieses Script vollautomatisch erledigt.

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