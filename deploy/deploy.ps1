# ==========================================
# VICC Praxisarbeit – Cloudbasierter IT Service Monitor
# Automatisierte Azure-Bereitstellung
#
# Dieses Skript erstellt die für den IT Service Monitor benötigten
# Azure-Ressourcen und konfiguriert die Web App mit dem öffentlichen
# Docker-Hub-Image der Anwendung.
# ==========================================

$ErrorActionPreference = "Stop"

# Zentrale Konfiguration der Azure-Ressourcen und des Container-Images
$resourceGroup  = "rg-vicc-rafiz"
$location       = "switzerlandnorth"
$appServicePlan = "asp-vicc-rafiz"
$dockerImage    = "ipsorafiz/vicc-cloud-app:1.2"

$random = Get-Random -Minimum 10000 -Maximum 99999
$webAppName = "vicc-rafiz-$random"

# Führt Azure-CLI-Befehle aus und beendet das Skript bei einem Fehler.
function Invoke-AzureCli {
    param(
        [Parameter(Mandatory=$true)]
        [scriptblock]$Command
    )

    & $Command

    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "FEHLER: Azure CLI Befehl fehlgeschlagen." -ForegroundColor Red
        exit $LASTEXITCODE
    }
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " VICC Azure Deployment" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Prüft, ob eine gültige Azure-CLI-Anmeldung vorhanden ist.
Write-Host "`n[1/5] Azure Anmeldung wird geprüft..." -ForegroundColor Yellow
Invoke-AzureCli { az account show --output none }

# Erstellt die Resource Group in der definierten Azure-Region
# beziehungsweise bestätigt die bestehende Konfiguration.
Write-Host "[2/5] Resource Group wird erstellt/geprüft..." -ForegroundColor Yellow
Invoke-AzureCli {
    az group create `
        --name $resourceGroup `
        --location $location `
        --output none
}

# Erstellt den Linux App Service Plan im kostenlosen F1-Tarif.
Write-Host "[3/5] App Service Plan wird erstellt..." -ForegroundColor Yellow
Invoke-AzureCli {
    az appservice plan create `
        --name $appServicePlan `
        --resource-group $resourceGroup `
        --location $location `
        --sku F1 `
        --is-linux `
        --output none
}

# Erstellt die Web App mit einem zufällig generierten, eindeutigen Namen
# und weist ihr das definierte Docker-Hub-Image zu.
Write-Host "[4/5] Web App mit Docker Image wird erstellt..." -ForegroundColor Yellow
Invoke-AzureCli {
    az webapp create `
        --name $webAppName `
        --resource-group $resourceGroup `
        --plan $appServicePlan `
        --container-image-name $dockerImage `
        --output none
}

# Erzwingt HTTPS und startet die Web App abschliessend neu.
Write-Host "[5/5] HTTPS wird aktiviert und Anwendung gestartet..." -ForegroundColor Yellow

Invoke-AzureCli {
    az webapp update `
        --name $webAppName `
        --resource-group $resourceGroup `
        --https-only true `
        --output none
}

Invoke-AzureCli {
    az webapp restart `
        --name $webAppName `
        --resource-group $resourceGroup `
        --output none
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host " Deployment erfolgreich!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Region: $location"
Write-Host "Resource Group: $resourceGroup"
Write-Host "App Service Plan: $appServicePlan"
Write-Host "Web App: $webAppName"
Write-Host ""
Write-Host "Webseite:" -ForegroundColor Cyan
Write-Host "https://$webAppName.azurewebsites.net"
Write-Host ""
Write-Host "API:" -ForegroundColor Cyan
Write-Host "https://$webAppName.azurewebsites.net/api/status"
Write-Host ""
