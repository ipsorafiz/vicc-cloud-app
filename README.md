# Cloudbasierter IT Service Monitor

Praxisarbeit im Fach Virtualisierung und Cloud Computing (VICC).

## Projektübersicht

Dieses Projekt demonstriert die automatisierte Bereitstellung einer containerisierten und konfigurierbaren Monitoring-Anwendung auf Microsoft Azure.

Die entwickelte Anwendung überwacht konfigurierte HTTP-/HTTPS-Endpunkte und stellt deren aktuellen Zustand über eine Weboberfläche sowie eine REST-API bereit.

Die Anwendung wird als einfache cloudbasierte SaaS-Lösung über Microsoft Azure App Service bereitgestellt.

## Funktionen

Der IT Service Monitor bietet folgende Funktionen:

- Automatische Prüfung konfigurierter HTTP-/HTTPS-Endpunkte
- Ermittlung des HTTP-Statuscodes
- Messung der Antwortzeit
- Automatische Bewertung des Servicezustands
- Gesamtstatus aller überwachten Services
- REST-API unter `/api/status`
- Health-Endpoint unter `/health`
- Konfiguration der überwachten Services über `services.json`
- Automatisierte Bereitstellung der Azure-Infrastruktur

## Statuswerte

Die Anwendung unterscheidet zwischen drei Zuständen:

- `Online` – Service ist erreichbar und antwortet innerhalb der definierten Reaktionszeit
- `Eingeschränkt` – Service ist erreichbar, weist jedoch beispielsweise eine erhöhte Antwortzeit auf
- `Offline` – Service ist nicht erreichbar oder liefert einen entsprechenden Fehlerstatus

## Aktuell konfigurierte Monitoring-Ziele

- Microsoft 365
- Microsoft Azure
- GitHub
- Docker Hub
- Demo Störungsdienst

Der Demo Störungsdienst liefert bewusst einen HTTP-503-Status, um einen Ausfall innerhalb der Anwendung reproduzierbar darzustellen.

## Konfiguration

Die zu überwachenden Services werden in `app/services.json` definiert.

Pro Service können unter anderem folgende Werte konfiguriert werden:

- Name
- URL
- Timeout

Neue Monitoring-Ziele können dadurch ergänzt werden, ohne die Programmlogik der Anwendung anzupassen.

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
  - `app.py` – Monitoring-Logik, Weboberfläche und REST-API
  - `services.json` – Konfiguration der überwachten Services
  - `Dockerfile` – Definition des Container Images
  - `requirements.txt` – benötigte Python-Abhängigkeiten

- `deploy/`
  - `deploy.ps1` – automatisierte Bereitstellung der Azure-Infrastruktur

## Container Image

Docker Hub:

`ipsorafiz/vicc-cloud-app:1.2`

## Azure Deployment

Das Deployment-Script erstellt beziehungsweise konfiguriert:

- Azure Resource Group
- Linux App Service Plan
- Azure Web App
- Container Deployment
- HTTPS

Das aktuelle Container Image wird aus Docker Hub geladen und im Azure App Service betrieben.

## Endpunkte

Weboberfläche:

`/`

REST-API:

`/api/status`

Health Check:

`/health`

## Hinweise zum Prototyp

Der aktuelle Service Monitor überprüft HTTP-/HTTPS-Endpunkte.

Eine zukünftige Erweiterung könnte zusätzliche Monitoring-Typen wie Datenbanken, TCP-Dienste, interne Systeme oder Schnittstellen bestehender Monitoring-Lösungen berücksichtigen.

Für einen produktiven internen Einsatz wäre zusätzlich eine Authentifizierung beziehungsweise Zugriffsbeschränkung sinnvoll.

## Version

Aktuelle Version: `1.2`

## Autor

Rafiz Krasniqi