#!/usr/bin/env bash
# ============================================
#   Arcan-Ai — Fine-tuning (Unix/Linux/macOS)
#   Adapte le modèle de base à la génération
#   de leçons éducatives personnalisées.
#
#   Prérequis : Ollama installé localement
#   https://ollama.ai/download
# ============================================
set -e

DATASET="data/sample_lessons.jsonl"
BASE_MODEL="mistralai/Mistral-7B-Instruct-v0.1"
OUTPUT_MODEL="arcan-ai-tutor"
STEPS=100

echo ""
echo "============================================"
echo "   Arcan-Ai  |  Fine-tuning du modèle"
echo "============================================"
echo ""

# --- Vérifier Ollama ---
echo "[1/3] Vérification d'Ollama..."
if ! command -v ollama &>/dev/null; then
    echo "  ✗ Ollama n'est pas installé !"
    echo "    Installez-le : curl -fsSL https://ollama.ai/install.sh | sh"
    exit 1
fi
echo "  ✓ Ollama détecté : $(ollama --version 2>&1)"

# --- Vérifier le dataset ---
echo ""
echo "[2/3] Vérification du dataset..."
if [ ! -f "$DATASET" ]; then
    echo "  ✗ Dataset introuvable : $DATASET"
    echo "    Créez le dossier 'data' et placez-y sample_lessons.jsonl"
    echo "    Format attendu (une ligne par exemple) :"
    echo '    {"prompt":"<sujet>","completion":"<leçon générée>"}'
    exit 1
fi
echo "  ✓ Dataset trouvé : $DATASET"

# --- Fine-tuning ---
echo ""
echo "[3/3] Lancement du fine-tuning..."
echo "  Modèle de base  : $BASE_MODEL"
echo "  Modèle de sortie: $OUTPUT_MODEL"
echo "  Steps           : $STEPS"
echo ""

ollama finetune "$BASE_MODEL" "$DATASET" --steps "$STEPS" --output "$OUTPUT_MODEL"

echo ""
echo "  ✓ Fine-tuning terminé !"
echo ""
echo "  Pour utiliser ce modèle, mettez à jour votre .env :"
echo "  FINETUNED_MODEL=$OUTPUT_MODEL"
echo ""
echo "  Test rapide :"
echo "  ollama run $OUTPUT_MODEL \"Génère une leçon sur les dérivées pour un lycéen\""
echo ""
echo "============================================"
echo "  Relancez l'application pour utiliser"
echo "  le nouveau modèle."
echo "============================================"
echo ""
