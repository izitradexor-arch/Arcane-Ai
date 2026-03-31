#!/usr/bin/env bash
set -euo pipefail

# --- CONFIG LOG ---
LOG_FILE="arcan-ai.log"

log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] $1" | tee -a "$LOG_FILE"
}

warn() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] [WARN] $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] $1" | tee -a "$LOG_FILE"
}

# Active le mode debug bash (affiche chaque commande exécutée)
DEBUG=${DEBUG:-false}
if [ "$DEBUG" = true ]; then
    set -x
    log "Mode DEBUG activé"
fi

echo ""
echo "============================================"
echo "        Arcan-Ai  |  Tuteur IA"
echo "============================================"
echo ""

log "Démarrage du script"

# --- Python ---
log "[1/4] Vérification de Python..."
if ! command -v python3 &>/dev/null; then
    error "Python 3 non installé"
    exit 1
fi
log "Python détecté : $(python3 --version)"

# --- Fichiers ---
log "[2/4] Vérification des fichiers..."
for f in app.py lesson_generator.py index.html requirements.txt; do
    if [ ! -f "$f" ]; then
        error "Fichier manquant : $f"
        exit 1
    else
        log "OK : $f"
    fi
done

# --- .env ---
log "[3/4] Vérification .env..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        warn ".env créé automatiquement"
        echo ""
        echo "  IMPORTANT : Éditez .env et renseignez votre OLLAMA_API_KEY :"
        echo "  nano .env"
        echo ""
        read -rp "  Appuyez sur Entrée après avoir édité .env..."
    else
        error ".env et .env.example absents"
        exit 1
    fi
fi

# Debug contenu (sans afficher la clé complète)
log "Chargement des variables .env"
grep -v "API_KEY" .env | tee -a "$LOG_FILE"

if ! grep -qE "OLLAMA_API_KEY=\S+" .env; then
    error "OLLAMA_API_KEY non définie"
    exit 1
fi

log "Clé API détectée"

# --- Dépendances ---
log "[4/4] Vérification des dépendances..."
if ! python3 -c "import flask" &>/dev/null; then
    warn "Flask non installé → installation..."
    pip3 install -r requirements.txt | tee -a "$LOG_FILE"
else
    log "Dépendances déjà installées"
fi

# --- Port debug ---
PORT=5000
if command -v lsof &>/dev/null; then
    if lsof -i:$PORT &>/dev/null; then
        warn "Le port $PORT est déjà utilisé !"
        lsof -i:$PORT | tee -a "$LOG_FILE"
    fi
elif command -v ss &>/dev/null; then
    if ss -tlnp | grep -q ":$PORT "; then
        warn "Le port $PORT est déjà utilisé !"
    fi
fi

# --- Démarrage ---
log "Lancement de l'application Flask..."

echo ""
echo "============================================"
echo "  Application prête !"
echo "============================================"
echo ""

python3 app.py 2>&1 | tee -a "$LOG_FILE"
