# Cloudbasiertes Statusportal für IT-Services

Praxisarbeit im Fach Virtualisierung und Cloud Computing (VICC).

## Projektübersicht

Dieses Projekt demonstriert die automatisierte Bereitstellung einer containerisierten Webanwendung auf Microsoft Azure.

Die entwickelte Anwendung ist ein cloudbasiertes Statusportal für IT-Services. Sie stellt den Status verschiedener Services über eine Weboberfläche dar und bietet zusätzlich eine REST-API.

## Funktionen

Die Anwendung stellt folgende Funktionen bereit:

- Statusübersicht verschiedener IT-Services
- Gesamtstatus der Umgebung
- Statuswerte Online, Eingeschränkt und Offline
- REST-API unter `/api/status`
- Health-Endpoint unter `/health`
- Anzeige von Version und Umgebung

Aktuell werden folgende Services dargestellt:

- Microsoft 365
- Netzwerk / WLAN
- Fileservice
- Druckservice
- Service Desk

Die Statuswerte werden im Rahmen des Prototyps aus einer Konfigurationsdatei geladen.

## Verwendete Technologien

- Microsoft Azure App Service
- Docker
- Docker Hub
- PowerShell
- Azure CLI
- Python / Flask
- Gunicorn
- GitHub

## Projektstruktur

- `app/`
  - `app.py` – Webanwendung und REST-API
  - `services.json` – Statusinformationen der dargestellten IT-Services
  - `Dockerfile` – Definition des Container Images
  - `requirements.txt` – benötigte Python-Abhängigkeiten

- `deploy/`
  - `deploy.ps1` – automatisierte Bereitstellung der Azure-Infrastruktur

## Container Image

Docker Hub:

`ipsorafiz/vicc-cloud-app:1.1`

## Deployment

Voraussetzungen:

- Azure CLI
- Azure Subscription
- PowerShell

Das Deployment erfolgt mit:

`deploy/deploy.ps1`

Das Script erstellt bzw. konfiguriert:

- Azure Resource Group
- Linux App Service Plan
- Azure Web App
- Container Deployment
- HTTPS

## Bereitgestellte Endpunkte

Weboberfläche:

`/`

REST-API:

`/api/status`

Health Check:

`/health`

## Hinweise zum Prototyp

Für einen produktiven Einsatz als internes Statusportal wäre eine Authentifizierung bzw. Zugriffsbeschränkung erforderlich.

Diese ist im Rahmen der Praxisarbeit bewusst nicht umgesetzt, da der Schwerpunkt auf der Cloud-Infrastruktur, der automatisierten Bereitstellung sowie der Betrachtung von Skalierbarkeit, Hochverfügbarkeit und Portierbarkeit liegt.

## Autor

Rafiz Krasniqi
