#!/usr/bin/env bash
# ============================================
#   Arcan-Ai — Setup & Test (Linux/macOS)
#   Usage : ./setup_and_test.sh
# ============================================
set -e

echo ""
echo "============================================"
echo "       Arcan-Ai  |  Setup & Test"
echo "============================================"
echo ""

# --- Étape 1 : Python ---
echo "[1/5] Vérification de Python..."
if ! command -v python3 &>/dev/null; then
    echo "  ✗ Python 3 n'est pas installé !"
    echo "    Ubuntu/Debian : sudo apt install python3 python3-pip"
    echo "    Fedora        : sudo dnf install python3 python3-pip"
    exit 1
fi
echo "  ✓ $(python3 --version)"

# --- Étape 2 : Fichiers obligatoires ---
echo ""
echo "[2/5] Vérification des fichiers du projet..."
missing=()
for f in app.py lesson_generator.py index.html requirements.txt; do
    [ ! -f "$f" ] && missing+=("$f")
done
if [ ${#missing[@]} -gt 0 ]; then
    echo "  ✗ Fichiers manquants : ${missing[*]}"
    echo "    Assurez-vous d'être dans le dossier arcan-ai/"
    exit 1
fi
echo "  ✓ Tous les fichiers sont présents"

# --- Étape 3 : Fichier .env ---
echo ""
echo "[3/5] Vérification de la configuration .env..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "  [!] .env créé depuis .env.example"
    else
        echo "  ✗ .env et .env.example sont tous les deux manquants !"
        exit 1
    fi
    echo ""
    echo "  IMPORTANT : Éditez .env et renseignez votre OLLAMA_API_KEY :"
    echo "  nano .env"
    echo ""
    read -rp "  Appuyez sur Entrée après avoir édité .env..."
fi

if grep -q "OLLAMA_API_KEY=votre_cle_api_ici" .env || ! grep -qE "OLLAMA_API_KEY=\S+" .env; then
    echo "  ✗ OLLAMA_API_KEY non renseignée dans .env !"
    echo "    Éditez avec : nano .env"
    exit 1
fi
echo "  ✓ Clé API détectée dans .env"

# --- Étape 4 : Dépendances Python ---
echo ""
echo "[4/5] Installation des dépendances Python..."
pip3 install -r requirements.txt --quiet
echo "  ✓ Dépendances installées"

# --- Étape 5 : Test du module Python ---
echo ""
echo "[5/5] Test du module lesson_generator..."
result=$(python3 - <<'EOF'
import os, sys
from dotenv import load_dotenv
load_dotenv()
try:
    from lesson_generator import build_prompt, DEFAULT_MODEL
    p = build_prompt('Mathematiques', 'Lycee', 'Visuel', ['Algebre'])
    print(f"OK — modele: {DEFAULT_MODEL} | prompt: {len(p)} car.")
except Exception as e:
    print(f"ERREUR : {e}")
    sys.exit(1)
EOF
)

if [ $? -eq 0 ]; then
    echo "  ✓ $result"
else
    echo "  ✗ $result"
    exit 1
fi

# --- Résumé ---
echo ""
echo "============================================"
echo "  Setup terminé avec succès !"
echo "============================================"
echo ""
echo "  Lancez l'application avec :"
echo "  ./start.sh"
echo ""
echo "  Puis ouvrez : http://localhost:5000"
echo ""
