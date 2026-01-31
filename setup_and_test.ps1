# Script d'installation et de test pour le générateur d'itinéraires
# Enregistrez ce fichier sous : setup_and_test.ps1

Write-Host "=== Installation et test du générateur d'itinéraires ===" -ForegroundColor Cyan

# Vérifier si Ollama est installé
Write-Host "`nÉtape 1: Vérification d'Ollama..." -ForegroundColor Yellow
try {
    $ollamaVersion = ollama --version 2>$null
    Write-Host "✓ Ollama est installé: $ollamaVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Ollama n'est pas installé!" -ForegroundColor Red
    Write-Host "Téléchargez-le depuis: https://ollama.ai/download" -ForegroundColor Yellow
    Write-Host "Après l'installation, redémarrez PowerShell et relancez ce script." -ForegroundColor Yellow
    exit 1
}

# Vérifier si Python est installé
Write-Host "`nÉtape 2: Vérification de Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>$null
    Write-Host "✓ Python est installé: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python n'est pas installé!" -ForegroundColor Red
    exit 1
}

# Installer le SDK Ollama Python
Write-Host "`nÉtape 3: Installation du SDK Ollama Python..." -ForegroundColor Yellow
try {
    pip install ollama --quiet
    Write-Host "✓ SDK Ollama Python installé" -ForegroundColor Green
} catch {
    Write-Host "⚠ Erreur lors de l'installation du SDK (non critique)" -ForegroundColor Yellow
}

# Vérifier les modèles disponibles
Write-Host "`nÉtape 4: Vérification des modèles..." -ForegroundColor Yellow
$models = ollama list 2>$null
Write-Host $models

# Proposer de télécharger un modèle si aucun n'est disponible
if ($models -notmatch "mistral") {
    Write-Host "`n⚠ Le modèle 'mistral:7b-instruct' n'est pas disponible" -ForegroundColor Yellow
    $response = Read-Host "Voulez-vous le télécharger maintenant? (o/N)"
    if ($response -eq "o" -or $response -eq "O") {
        Write-Host "Téléchargement du modèle (cela peut prendre plusieurs minutes)..." -ForegroundColor Yellow
        ollama pull mistral:7b-instruct
        Write-Host "✓ Modèle téléchargé" -ForegroundColor Green
    } else {
        Write-Host "Vous devrez télécharger un modèle avec: ollama pull mistral:7b-instruct" -ForegroundColor Yellow
    }
}

# Test rapide
Write-Host "`nÉtape 5: Test rapide d'Ollama..." -ForegroundColor Yellow
$testResponse = ollama run mistral:7b-instruct "Say 'OK' if you work" --verbose=false 2>$null
if ($testResponse) {
    Write-Host "✓ Ollama fonctionne correctement" -ForegroundColor Green
} else {
    Write-Host "⚠ Impossible de tester Ollama" -ForegroundColor Yellow
}

Write-Host "`n=== Installation terminée ===" -ForegroundColor Cyan
Write-Host "`nVous pouvez maintenant exécuter:" -ForegroundColor Green
Write-Host "python c:/Users/BoS/Desktop/llm/my-travel-itinerary-olama/src/pipeline.py" -ForegroundColor White
