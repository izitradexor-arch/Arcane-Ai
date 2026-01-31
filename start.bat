@echo off
REM Script de demarrage rapide pour Voyageur AI
REM Double-cliquez sur ce fichier pour demarrer l'application

echo ============================================
echo    Voyageur AI - Generateur d'Itineraires
echo ============================================
echo.

REM Verifier si Python est installe
python --version >nul 2>nul
if %errorlevel% neq 0 (
    echo [X] Python n'est pas installe!
    echo Installez Python depuis: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Verifier si Ollama est installe
where ollama >nul 2>nul
if %errorlevel% neq 0 (
    echo [X] Ollama n'est pas installe!
    echo Installez Ollama depuis: https://ollama.ai/download
    pause
    exit /b 1
)

REM Verifier si pipeline.py existe
if not exist "pipeline.py" (
    echo [!] ATTENTION: pipeline.py est manquant!
    echo.
    echo Renommez 'itinerary_generator.py' en 'pipeline.py'
    echo ou copiez son contenu dans pipeline.py
    echo.
    pause
    exit /b 1
)

REM Installer les dependances si necessaire
if not exist "venv" (
    echo [1/3] Installation des dependances...
    pip install -q -r requirements.txt
    if %errorlevel% neq 0 (
        echo [X] Erreur lors de l'installation des dependances
        pause
        exit /b 1
    )
    echo [OK] Dependances installees
)

REM Verifier qu'un modele est disponible
echo.
echo [2/3] Verification du modele Ollama...
ollama list | find "mistral" >nul
if %errorlevel% neq 0 (
    echo [!] Le modele Mistral n'est pas installe
    echo.
    set /p download="Voulez-vous le telecharger maintenant? (o/N): "
    if /i "%download%"=="o" (
        echo Telechargement en cours (plusieurs minutes)...
        ollama pull mistral:7b-instruct
        echo [OK] Modele telecharge
    ) else (
        echo.
        echo [!] Sans modele, l'application ne fonctionnera pas
        echo Telechargez-le manuellement: ollama pull mistral:7b-instruct
        echo.
        pause
        exit /b 1
    )
) else (
    echo [OK] Modele Mistral disponible
)

REM Demarrer le serveur
echo.
echo [3/3] Demarrage du serveur...
echo.
echo ============================================
echo  Application prete!
echo ============================================
echo.
echo  Ouvrez votre navigateur sur:
echo  http://localhost:5000
echo.
echo  Appuyez sur Ctrl+C pour arreter le serveur
echo ============================================
echo.

python app.py

pause
