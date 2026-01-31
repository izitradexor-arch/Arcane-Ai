# PowerShell script pour télécharger et fine-tuner un modèle avec Olama
# Exécuter depuis le dossier du projet

# 1) Télécharger le modèle de base
olama download mistralai/Mistral-7B-Instruct-v0.1

# 2) Lancer le fine-tuning (exemple)
# Remplacez `data/sample_itineraries.jsonl` par votre dataset
olama finetune mistralai/Mistral-7B-Instruct-v0.1 data/sample_itineraries.jsonl --steps 100 --output my-travel-itinerary-model

# 3) Après fine-tuning, testez la génération via la CLI ou le script Python
# olama generate --model my-travel-itinerary-model --prompt "Create a 3-day itinerary for Rome with interests in history, food"
