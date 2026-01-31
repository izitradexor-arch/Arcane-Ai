@echo off
REM Script de demarrage avec API Ollama Cloud
REM Double-cliquez pour lancer l'application

echo ============================================
echo    Voyageur AI - Mode Cloud API
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

REM Verifier si les dependances sont installees
echo [1/3] Verification des dependances...
pip show flask >nul 2>nul
if %errorlevel% neq 0 (
    echo Installation des dependances...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [X] Erreur lors de l'installation des dependances
        pause
        exit /b 1
    )
)
echo [OK] Dependances installees

REM Verifier que le fichier .env existe
echo.
echo [2/3] Verification de la configuration...
if not exist ".env" (
    echo [!] Fichier .env manquant
    echo Creation du fichier .env...
    copy .env.example .env
    echo.
    echo IMPORTANT: Editez le fichier .env et ajoutez votre cle API Ollama
    echo.
    pause
)
echo [OK] Configuration trouvee

REM Verifier que pipeline.py existe
if not exist "pipeline.py" (
    echo [!] ATTENTION: pipeline.py manquant!
    echo Renommez itinerary_generator.py en pipeline.py
    pause
    exit /b 1
)

REM Demarrer le serveur
echo.
echo [3/3] Demarrage du serveur...
echo.
echo ============================================
echo  Application prete! (Mode Cloud API)
echo ============================================
echo.
echo  Ouvrez votre navigateur sur:
echo  http://localhost:5000
echo.
echo  API Endpoint:
echo  http://localhost:5000/api/generate
echo.
echo  Appuyez sur Ctrl+C pour arreter
echo ============================================
echo.

python app.py

pause
