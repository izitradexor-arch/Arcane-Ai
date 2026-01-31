# 🚀 Guide de Déploiement - Voyageur AI

Votre application est maintenant configurée pour utiliser l'API Ollama Cloud et peut être déployée facilement !

## 📋 Modifications Effectuées

### ✅ Code Backend
- **pipeline.py** : Utilise maintenant l'API Ollama Cloud au lieu de l'installation locale
- **app.py** : Configure CORS et variables d'environnement pour le déploiement
- **requirements.txt** : Dépendances mises à jour (requests, gunicorn, python-dotenv)

### ✅ Configuration
- **.env** : Stocke votre clé API de manière sécurisée (⚠️ NE PAS COMMITER)
- **.gitignore** : Protège vos fichiers sensibles
- **Procfile** : Configuration pour Heroku
- **runtime.txt** : Version de Python

### ✅ Frontend
- **index_v2.html** : URL API dynamique (fonctionne en local ET en production)

---

## 🔧 Test en Local

### 1. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 2. Configurer les variables d'environnement
Copiez `.env.example` vers `.env` et ajoutez votre clé API :
```bash
OLLAMA_API_KEY=fc289982b86c43a8932b374295b7bd7b.fLzWxh3aqp2BQTPMo04iJzKT
```

### 3. Lancer le serveur
```bash
python app.py
```

### 4. Tester
Ouvrez http://localhost:5000 dans votre navigateur.

---

## 🌐 Déploiement sur Heroku

### Prérequis
- Compte Heroku (gratuit) : https://signup.heroku.com/
- Heroku CLI installé : https://devcenter.heroku.com/articles/heroku-cli

### Étape 1 : Initialiser Git
```bash
cd C:\Users\BoS\Desktop\llm\my-travel-itinerary-olama
git init
git add .
git commit -m "Initial commit - Voyageur AI"
```

### Étape 2 : Créer l'application Heroku
```bash
heroku login
heroku create voyageur-ai-app
```
*(Remplacez `voyageur-ai-app` par un nom unique)*

### Étape 3 : Configurer les variables d'environnement
```bash
heroku config:set OLLAMA_API_KEY=fc289982b86c43a8932b374295b7bd7b.fLzWxh3aqp2BQTPMo04iJzKT
heroku config:set OLLAMA_API_URL=https://api.ollama.cloud/v1/chat/completions
heroku config:set FLASK_ENV=production
```

### Étape 4 : Déployer
```bash
git push heroku main
```

### Étape 5 : Ouvrir l'application
```bash
heroku open
```

---

## 🚀 Déploiement sur Render

### Étape 1 : Créer un compte
Allez sur https://render.com et créez un compte gratuit.

### Étape 2 : Nouveau Web Service
1. Cliquez sur "New +" → "Web Service"
2. Connectez votre repository GitHub/GitLab
3. Ou utilisez "Public Git Repository" et entrez l'URL de votre repo

### Étape 3 : Configuration
- **Name** : `voyageur-ai`
- **Environment** : `Python`
- **Build Command** : `pip install -r requirements.txt`
- **Start Command** : `gunicorn app:app`

### Étape 4 : Variables d'environnement
Ajoutez dans "Environment Variables" :
```
OLLAMA_API_KEY = fc289982b86c43a8932b374295b7bd7b.fLzWxh3aqp2BQTPMo04iJzKT
OLLAMA_API_URL = https://api.ollama.cloud/v1/chat/completions
FLASK_ENV = production
```

### Étape 5 : Déployer
Cliquez sur "Create Web Service" et attendez le déploiement !

---

## ☁️ Déploiement sur Vercel

### Étape 1 : Installer Vercel CLI
```bash
npm install -g vercel
```

### Étape 2 : Se connecter
```bash
vercel login
```

### Étape 3 : Déployer
```bash
cd C:\Users\BoS\Desktop\llm\my-travel-itinerary-olama
vercel
```

### Étape 4 : Configurer les variables
```bash
vercel env add OLLAMA_API_KEY
# Entrez: fc289982b86c43a8932b374295b7bd7b.fLzWxh3aqp2BQTPMo04iJzKT

vercel env add OLLAMA_API_URL
# Entrez: https://api.ollama.cloud/v1/chat/completions
```

---

## 🐳 Déploiement avec Docker

### Créer un Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### Build et Run
```bash
docker build -t voyageur-ai .
docker run -p 5000:5000 \
  -e OLLAMA_API_KEY=fc289982b86c43a8932b374295b7bd7b.fLzWxh3aqp2BQTPMo04iJzKT \
  -e OLLAMA_API_URL=https://api.ollama.cloud/v1/chat/completions \
  voyageur-ai
```

---

## 🔒 Sécurité - IMPORTANT

### ⚠️ NE JAMAIS commiter le fichier .env
Le fichier `.gitignore` protège `.env`, mais vérifiez toujours :
```bash
git status
# .env ne doit PAS apparaître
```

### ✅ Variables d'environnement en production
Toujours configurer les variables via :
- Heroku : `heroku config:set`
- Render : Dashboard → Environment Variables
- Vercel : `vercel env add`

### 🔐 Rotation de la clé API
Si votre clé est compromise :
1. Générez une nouvelle clé sur Ollama Cloud
2. Mettez à jour les variables d'environnement
3. Redéployez l'application

---

## 📁 Structure Finale

```
my-travel-itinerary-olama/
├── app.py                    # Backend Flask
├── pipeline.py               # Logique Ollama Cloud API
├── requirements.txt          # Dépendances Python
├── Procfile                  # Configuration Heroku
├── runtime.txt               # Version Python
├── .env                      # Variables locales (⚠️ NE PAS COMMITER)
├── .env.example              # Template de configuration
├── .gitignore                # Fichiers à ignorer
└── static/
    └── index.html            # Interface web (renommer index_v2.html)
```

---

## 🧪 Tests Post-Déploiement

### Test 1 : Santé de l'API
```bash
curl https://votre-app.herokuapp.com/api/health
```
Résultat attendu :
```json
{"status": "ok", "message": "API du générateur d'itinéraires opérationnelle"}
```

### Test 2 : Génération d'itinéraire
```bash
curl -X POST https://votre-app.herokuapp.com/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Paris",
    "duration": 3,
    "interests": ["art", "food"],
    "budget": 1500
  }'
```

### Test 3 : Interface Web
Ouvrez `https://votre-app.herokuapp.com` et testez la génération.

---

## 🐛 Dépannage

### Erreur : "API Key not configured"
- Vérifiez que `OLLAMA_API_KEY` est bien définie
- Relancez le serveur après modification du .env

### Erreur 500 sur l'API
- Vérifiez les logs : `heroku logs --tail`
- Testez l'API Ollama directement
- Vérifiez la validité de votre clé API

### L'application ne se charge pas
- Vérifiez que `static/index.html` existe
- Assurez-vous que tous les fichiers sont commités

### Timeout lors de la génération
- Normal pour les premières requêtes
- Ajustez le timeout si nécessaire dans `pipeline.py`

---

## 📊 Monitoring

### Heroku
```bash
heroku logs --tail
heroku ps
```

### Render
Dashboard → Logs

### Localement
Les logs s'affichent dans le terminal où vous avez lancé `python app.py`

---

## 💰 Coûts

### API Ollama Cloud
- Vérifiez votre plan sur https://ollama.cloud/pricing
- Surveillez votre usage

### Hébergement
- **Heroku** : Plan gratuit disponible (limité)
- **Render** : Plan gratuit disponible
- **Vercel** : Plan gratuit pour les projets personnels

---

## 🎉 Votre Application est Prête !

Votre générateur d'itinéraires fonctionne maintenant avec l'API Ollama Cloud et peut être déployé sur n'importe quelle plateforme !

### Checklist Finale
- [ ] Tests en local fonctionnent
- [ ] `.env` est dans `.gitignore`
- [ ] Variables d'environnement configurées en production
- [ ] Application déployée et accessible
- [ ] Tests post-déploiement effectués

**Bon déploiement ! 🚀✈️**
