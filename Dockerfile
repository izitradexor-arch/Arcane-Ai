FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tous les fichiers de l'application
COPY . .

# Exposer le port
EXPOSE 5000

# Variables d'environnement par défaut
ENV FLASK_ENV=production
ENV FLASK_DEBUG=False
ENV PORT=5000

# Commande de démarrage avec gunicorn
CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120 app:app
