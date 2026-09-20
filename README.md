# VICC Cloud Application

Praxisarbeit im Fach Virtualisierung und Cloud Computing (VICC).

## Projektübersicht

Dieses Projekt demonstriert die automatisierte Bereitstellung einer containerisierten Webanwendung auf Microsoft Azure.

Die Anwendung stellt zwei Zugriffsmöglichkeiten bereit:

- Weboberfläche
- REST-API unter /api/status

## Verwendete Technologien

- Microsoft Azure App Service
- Docker
- Docker Hub
- PowerShell
- Azure CLI
- Python / Flask

## Projektstruktur

- app/ - Source Code, Dockerfile und Abhängigkeiten
- deploy/ - PowerShell-Script für die automatisierte Bereitstellung der Azure-Infrastruktur

## Container Image

Docker Hub:

ipsorafiz/vicc-cloud-app:1.0

## Deployment

Voraussetzungen:

- Azure CLI
- Azure Subscription
- PowerShell

Das Deployment erfolgt durch Ausführen von deploy/deploy.ps1.

Das Script erstellt bzw. konfiguriert:

- Azure Resource Group
- Linux App Service Plan
- Azure Web App
- Docker Container Deployment
- HTTPS

## Autor

Rafiz Krasniqi
