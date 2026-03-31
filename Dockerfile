FROM python:3.11-slim

# Répertoire de travail
WORKDIR /app

# Dépendances système minimales
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
# ⚠️  Ne jamais copier .env dans l'image — passez les secrets via --env-file ou variables d'environnement
COPY app.py lesson_generator.py index.html ./

# Port exposé
EXPOSE 5000

# Variables d'environnement par défaut (sans secrets)
ENV FLASK_DEBUG=False
ENV PORT=5000
ENV OLLAMA_HOST=https://ollama.com
ENV DEFAULT_MODEL=gpt-oss:120b-cloud
ENV FINETUNED_MODEL=gpt-oss:120b-cloud

# Démarrage avec gunicorn (production)
# OLLAMA_API_KEY doit être passée au moment du run :
#   docker run --env-file .env -p 5000:5000 arcan-ai
CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120 app:app
