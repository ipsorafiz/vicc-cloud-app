# ==========================================
# VICC Praxisarbeit
# Automatisiertes Azure Deployment
# ==========================================

$ErrorActionPreference = "Stop"

$resourceGroup  = "rg-vicc-rafiz"
$location       = "switzerlandnorth"
$appServicePlan = "asp-vicc-rafiz"
$dockerImage    = "ipsorafiz/vicc-cloud-app:1.2"

$random = Get-Random -Minimum 10000 -Maximum 99999
$webAppName = "vicc-rafiz-$random"

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

Write-Host "`n[1/5] Azure Anmeldung wird geprÃ¼ft..." -ForegroundColor Yellow
Invoke-AzureCli { az account show --output none }

Write-Host "[2/5] Resource Group wird erstellt/geprÃ¼ft..." -ForegroundColor Yellow
Invoke-AzureCli {
    az group create `
        --name $resourceGroup `
        --location $location `
        --output none
}

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

Write-Host "[4/5] Web App mit Docker Image wird erstellt..." -ForegroundColor Yellow
Invoke-AzureCli {
    az webapp create `
        --name $webAppName `
        --resource-group $resourceGroup `
        --plan $appServicePlan `
        --container-image-name $dockerImage `
        --output none
}

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
