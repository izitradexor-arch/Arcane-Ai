#!/usr/bin/env bash
# Script d'entraînement pour environnements Unix
set -e

# 1) Télécharger le modèle de base
olama download mistralai/Mistral-7B-Instruct-v0.1

# 2) Fine-tuning
olama finetune mistralai/Mistral-7B-Instruct-v0.1 data/sample_itineraries.jsonl --steps 100 --output my-travel-itinerary-model

# 3) Test de génération (exemple)
# olama generate --model my-travel-itinerary-model --prompt "Create a 3-day itinerary for Rome with interests in history, food"
