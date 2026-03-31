# ⟡ Arcan-Ai — Documentation Complète

## Table des Matières
1. [Vue d'ensemble](#vue-densemble)
2. [Architecture du Système](#architecture-du-système)
3. [Fonctionnement Détaillé](#fonctionnement-détaillé)
4. [Composants](#composants)
5. [Flux de Données](#flux-de-données)
6. [Configuration](#configuration)
7. [API Reference](#api-reference)
8. [Interface Utilisateur](#interface-utilisateur)
9. [Sécurité](#sécurité)
10. [Déploiement](#déploiement)

---

## Vue d'ensemble

**Arcan-Ai** est un tuteur éducatif personnalisé propulsé par l'intelligence artificielle. Il génère des leçons sur mesure en utilisant l'API Ollama Cloud, adaptées au niveau, au style d'apprentissage et aux préférences de chaque élève.

### Fonctionnalités Principales
- 🎓 Génération de leçons personnalisées par IA
- 🧠 Adaptation au style d'apprentissage (Visuel, Auditif, Kinesthésique, Lecture/Écriture)
- 📚 Couverture de multiples matières et niveaux
- ⏱️ Contrôle de la durée des sessions (15-180 minutes)
- 🎨 Interface utilisateur immersive et mystique

---

## Architecture du Système

```
┌─────────────────────────────────────────────────────────────┐
│                    NAVIGATEUR WEB                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              index.html (Frontend)                  │   │
│  │  - Formulaire de configuration                      │   │
│  │  - Affichage des leçons                             │   │
│  │  - Animations et effets visuels                     │   │
│  └───────────────────────┬─────────────────────────────┘   │
│                          │                                  │
│                          │ HTTP/HTTPS                       │
│                          ▼                                  │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    SERVEUR FLASK                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  app.py                             │   │
│  │  - Routes HTTP (/, /api/*)                          │   │
│  │  - Validation des requêtes                          │   │
│  │  - Gestion des erreurs                              │   │
│  │  - CORS                                             │   │
│  └───────────────────────┬─────────────────────────────┘   │
│                          │                                  │
│                          ▼                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            lesson_generator.py                      │   │
│  │  - Construction du prompt                           │   │
│  │  - Appel à l'API Ollama Cloud                       │   │
│  │  - Traitement de la réponse                         │   │
│  └───────────────────────┬─────────────────────────────┘   │
│                          │                                  │
└──────────────────────────┼──────────────────────────────────┘
                           │
                           │ HTTPS
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  OLLAMA CLOUD API                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  - Modèle: gpt-oss:120b-cloud                       │   │
│  │  - Génération de texte                              │   │
│  │  - Authentification par clé API                     │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Fonctionnement Détaillé

### 1. Démarrage de l'Application

Lors du lancement de `app.py`:

1. **Chargement des variables d'environnement** depuis `.env`
2. **Vérification de la clé API** Ollama (obligatoire)
3. **Initialisation du serveur Flask** avec CORS
4. **Démarrage du serveur** sur le port configuré (défaut: 5000)

```python
# Séquence de démarrage
load_dotenv()                    # Charge .env
OLLAMA_API_KEY = os.environ.get('OLLAMA_API_KEY')  # Vérifie la clé
app.run(debug=debug, host='0.0.0.0', port=port)    # Lance le serveur
```

### 2. Génération d'une Leçon

#### Étape 1: Soumission du Formulaire
L'utilisateur remplit le formulaire avec:
- **Matière** (ex: Mathématiques, Physique, Français)
- **Niveau** (ex: Collège, Lycée, Université)
- **Style d'apprentissage** (Visuel, Auditif, Kinesthésique, Lecture/Écriture)
- **Thèmes** (sélection multiple ou personnalisé)
- **Durée** (optionnel, 15-180 minutes)

#### Étape 2: Requête API
Le frontend envoie une requête POST à `/api/generate`:
```json
{
  "subject": "Mathématiques",
  "level": "Lycée",
  "learning_style": "Visuel",
  "topics": ["Algèbre", "Géométrie"],
  "duration": 60
}
```

#### Étape 3: Validation
Le serveur vérifie:
- Présence des champs obligatoires
- Validité de la durée (15-180 min)
- Format des données

#### Étape 4: Construction du Prompt
`lesson_generator.py` construit un prompt personnalisé:
- Instructions spécifiques au style d'apprentissage
- Structure de la leçon (intro, objectifs, contenu, exercices, résumé)
- Adaptation au niveau de l'élève

#### Étape 5: Appel à l'API Ollama
```python
client = Client(
    host=OLLAMA_HOST,  # https://ollama.com
    headers={'Authorization': f'Bearer {OLLAMA_API_KEY}'}
)
response = client.chat(
    model=model_name,  # gpt-oss:120b-cloud
    messages=[{'role': 'user', 'content': prompt}],
    stream=False
)
```

#### Étape 6: Affichage
Le frontend reçoit la leçon générée et l'affiche avec:
- Formatage Markdown
- Animations d'apparition
- Options de copie et téléchargement

---

## Composants

### 1. `app.py` — Serveur Flask

**Rôle**: Point d'entrée de l'application, gère les requêtes HTTP.

**Routes**:
| Route | Méthode | Description |
|-------|---------|-------------|
| `/` | GET | Sert la page HTML principale |
| `/api/generate` | POST | Génère une leçon personnalisée |
| `/api/models` | GET | Liste les modèles disponibles |
| `/api/health` | GET | Vérifie l'état de l'API |

**Fonctionnalités**:
- Chargement des variables d'environnement
- Configuration CORS pour les requêtes cross-origin
- Validation des données d'entrée
- Gestion des erreurs avec messages explicites
- Logging des générations

### 2. `lesson_generator.py` — Générateur de Leçons

**Rôle**: Logique métier de génération de leçons.

**Fonctions principales**:

#### `build_prompt(subject, level, learning_style, topics, duration)`
Construit le prompt optimisé pour l'IA.

**Paramètres**:
- `subject`: Matière enseignée
- `level`: Niveau de l'élève
- `learning_style`: Style d'apprentissage
- `topics`: Liste des thèmes à couvrir
- `duration`: Durée de la session (optionnel)

**Retourne**: Prompt formaté pour l'API Ollama

#### `generate_lesson(subject, level, learning_style, topics, duration, model_name)`
Génère la leçon via l'API Ollama.

**Paramètres**:
- Tous les paramètres de `build_prompt`
- `model_name`: Modèle à utiliser (défaut: gpt-oss:120b-cloud)

**Retourne**: Contenu de la leçon générée

**Styles d'apprentissage supportés**:
| Style | Instructions données à l'IA |
|-------|----------------------------|
| Visuel | Diagrammes, schémas, cartes mentales |
| Auditif | Analogies, répétitions, mnémoniques |
| Kinesthésique | Exercices pratiques, manipulations |
| Lecture/Écriture | Textes détaillés, listes, résumés |

### 3. `index.html` — Interface Utilisateur

**Rôle**: Frontend de l'application.

**Sections**:
1. **En-tête**: Titre et sous-titre mystique
2. **Cartes interactives**: Présentation des fonctionnalités
3. **Formulaire**: Configuration de la leçon
4. **Zone de chargement**: Animation pendant la génération
5. **Résultats**: Affichage de la leçon générée

**Technologies**:
- HTML5/CSS3
- JavaScript (vanilla)
- Markdown renderer (marked.js)
- Animations CSS avancées

---

## Flux de Données

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Utilisateur │────▶│   Frontend   │────▶│   Backend    │
│  (Navigateur)│     │ (index.html) │     │   (app.py)   │
└──────────────┘     └──────────────┘     └──────────────┘
       │                    │                    │
       │ 1. Remplit le      │                    │
       │    formulaire      │                    │
       │                    │ 2. POST /api/generate
       │                    │    {subject, level,│
       │                    │     learning_style,│
       │                    │     topics, duration}
       │                    │                    │
       │                    │                    │ 3. Valide les données
       │                    │                    │
       │                    │                    │ 4. Appelle lesson_generator
       │                    │                    │
       │                    │                    ▼
       │                    │            ┌──────────────┐
       │                    │            │ lesson_      │
       │                    │            │ generator.py │
       │                    │            └──────────────┘
       │                    │                    │
       │                    │                    │ 5. Construit le prompt
       │                    │                    │
       │                    │                    │ 6. POST https://ollama.com/api/chat
       │                    │                    │    Authorization: Bearer <API_KEY>
       │                    │                    │    {model, messages}
       │                    │                    │
       │                    │                    ▼
       │                    │            ┌──────────────┐
       │                    │            │ Ollama Cloud │
       │                    │            │     API      │
       │                    │            └──────────────┘
       │                    │                    │
       │                    │                    │ 7. Retourne la leçon
       │                    │                    │
       │                    │◀───────────────────┘
       │                    │ 8. JSON response
       │                    │    {success, lesson, ...}
       │                    │
       │◀───────────────────┘ 9. Affiche la leçon
       │ 10. Lit la leçon
```

---

## Configuration

### Variables d'Environnement

| Variable | Obligatoire | Défaut | Description |
|----------|-------------|--------|-------------|
| `OLLAMA_API_KEY` | ✅ Oui | — | Clé API Ollama Cloud |
| `OLLAMA_HOST` | Non | `https://ollama.com` | URL de l'instance Ollama |
| `DEFAULT_MODEL` | Non | `gpt-oss:120b-cloud` | Modèle par défaut |
| `FINETUNED_MODEL` | Non | `gpt-oss:120b-cloud` | Modèle fine-tuné |
| `PORT` | Non | `5000` | Port du serveur Flask |
| `FLASK_DEBUG` | Non | `False` | Mode debug Flask |

### Fichier `.env.example`
```bash
# Configuration Arcan-Ai
OLLAMA_API_KEY=your_api_key_here
OLLAMA_HOST=https://ollama.com
DEFAULT_MODEL=gpt-oss:120b-cloud
FINETUNED_MODEL=gpt-oss:120b-cloud
PORT=5000
FLASK_DEBUG=False
```

### Dépendances (`requirements.txt`)
```
flask>=3.0.0
flask-cors>=4.0.0
python-dotenv>=1.0.0
ollama>=0.6.1
```

---

## API Reference

### POST `/api/generate`

Génère une leçon personnalisée.

**Headers**:
```
Content-Type: application/json
```

**Body** (JSON):
```json
{
  "subject": "Mathématiques",        // Obligatoire
  "level": "Lycée",                  // Obligatoire
  "learning_style": "Visuel",        // Obligatoire
  "topics": ["Algèbre", "Géométrie"], // Obligatoire (array, min 1)
  "duration": 60,                    // Optionnel (15-180)
  "model": "gpt-oss:120b-cloud"     // Optionnel
}
```

**Réponse Succès** (200):
```json
{
  "success": true,
  "lesson": "# Leçon de Mathématiques\n\n## Introduction\n...",
  "subject": "Mathématiques",
  "level": "Lycée",
  "learning_style": "Visuel",
  "topics": ["Algèbre", "Géométrie"],
  "duration": 60
}
```

**Réponse Erreur** (400/500):
```json
{
  "success": false,
  "error": "Message d'erreur détaillé"
}
```

**Codes d'erreur**:
| Code | Cause |
|------|-------|
| 400 | Données manquantes ou invalides |
| 400 | Sujet manquant |
| 400 | Niveau manquant |
| 400 | Style d'apprentissage manquant |
| 400 | Aucun thème sélectionné |
| 400 | Durée hors limites (15-180) |
| 500 | Erreur lors de la génération |

### GET `/api/models`

Liste les modèles disponibles.

**Réponse** (200):
```json
{
  "models": ["gpt-oss:120b-cloud", "gpt-oss:120b-cloud"],
  "default": "gpt-oss:120b-cloud"
}
```

### GET `/api/health`

Vérifie l'état de l'API.

**Réponse** (200):
```json
{
  "status": "ok",
  "message": "Arcan-Ai opérationnel ✨"
}
```

---

## Interface Utilisateur

### Structure de la Page

1. **En-tête Mystique**
   - Titre avec effet de dégradé
   - Sous-titre poétique
   - Décorations animées

2. **Cartes Interactives (Hover Cards)**
   - 6 cartes présentant les fonctionnalités
   - Animation de retournement au survol
   - Contenu révélé progressivement

3. **Formulaire de Configuration**
   - Champ matière (texte)
   - Sélecteur de niveau
   - Sélecteur de style d'apprentissage
   - Sélection de thèmes (tags cliquables)
   - Ajout de thèmes personnalisés
   - Curseur de durée (15-180 min)

4. **Bouton de Génération**
   - Effet de brillance au survol
   - Animation de pulsation
   - Désactivé pendant le chargement

5. **Zone de Chargement**
   - Spinner animé
   - Messages de progression
   - Animation cosmique

6. **Résultats**
   - En-tête avec métadonnées
   - Contenu formaté en Markdown
   - Boutons d'action (copier, télécharger, nouvelle leçon)

### Animations CSS

| Animation | Description |
|-----------|-------------|
| `cosmicDrift` | Déplacement lent du fond étoilé |
| `nebulaFloat` | Flottement des nébuleuses |
| `particleFloat` | Particules montantes |
| `twinkle` | Scintillement des étoiles |
| `quantumSpin` | Rotation des spinners |
| `shimmer` | Effet de brillance |
| `fadeInUp` | Apparition vers le haut |
| `fadeInDown` | Apparition vers le bas |
| `shake` | Secousse pour les erreurs |
| `pulse` | Pulsation |
| `cardEntry` | Entrée des cartes |
| `revealItem` | Révélation des éléments |
| `glowRotate` | Rotation de la lueur |
| `sparkleFloat` | Flottement des étincelles |

---

## Sécurité

### Protection de la Clé API
- ✅ Chargée depuis `.env` (jamais en dur)
- ✅ Fichier `.env` exclu du versionnement (`.gitignore`)
- ✅ Transmise via headers HTTP sécurisés

### Validation des Entrées
- ✅ Vérification des champs obligatoires
- ✅ Validation de la durée (15-180 min)
- ✅ Type checking des données
- ✅ Sanitization des messages d'erreur

### CORS
- ✅ Configuration explicite des origines autorisées
- ✅ Méthodes HTTP restreintes (GET, POST, OPTIONS)
- ✅ Headers contrôlés (Content-Type)

### Recommandations Production
1. Restreindre les origines CORS à votre domaine
2. Utiliser HTTPS en production
3. Implémenter un rate limiting
4. Ajouter une authentification utilisateur
5. Logger les tentatives d'accès suspectes

---

## Déploiement

### Développement Local
```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Configurer l'environnement
cp .env.example .env
# Éditer .env avec votre clé API

# 3. Lancer l'application
python app.py

# 4. Ouvrir dans le navigateur
# http://localhost:5000
```

### Production avec Gunicorn
```bash
# Installer Gunicorn (déjà dans requirements.txt)
pip install gunicorn

# Lancer avec Gunicorn
gunicorn app:app --bind 0.0.0.0:5000 --workers 4
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "4"]
```

### Variables d'Environnement Production
```bash
OLLAMA_API_KEY=your_production_key
OLLAMA_HOST=https://ollama.com
DEFAULT_MODEL=gpt-oss:120b-cloud
PORT=5000
FLASK_DEBUG=False
```

---

## Dépannage

### Erreur: "OLLAMA_API_KEY manquante"
**Cause**: Fichier `.env` absent ou mal configuré.
**Solution**:
```bash
cp .env.example .env
# Éditer .env et ajouter votre clé API
```

### Erreur: "Aucune donnée fournie"
**Cause**: Requête POST sans body JSON.
**Solution**: Vérifier que le frontend envoie bien un JSON.

### Erreur: "La durée doit être entre 15 et 180 minutes"
**Cause**: Valeur de durée hors limites.
**Solution**: Ajuster la valeur dans le formulaire.

### Erreur API Ollama
**Cause**: Problème de connexion ou clé API invalide.
**Solution**:
1. Vérifier la connexion internet
2. Vérifier la validité de la clé API
3. Vérifier que le modèle est disponible

---

## Glossaire

| Terme | Définition |
|-------|------------|
| **Ollama Cloud** | Plateforme d'IA hébergeant les modèles de langage |
| **gpt-oss:120b-cloud** | Modèle de langage utilisé pour la génération |
| **Prompt** | Instructions envoyées à l'IA pour guider la génération |
| **Style d'apprentissage** | Méthode préférée d'absorption des connaissances |
| **CORS** | Mécanisme de sécurité pour les requêtes cross-origin |
| **Flask** | Framework web Python utilisé pour le backend |
| **Markdown** | Langage de balisage léger pour le formatage du texte |

---

## Support

Pour toute question ou problème:
1. Consulter cette documentation
2. Vérifier les logs du serveur
3. Tester l'endpoint `/api/health`
4. Vérifier la configuration `.env`

---

**Version**: 1.0.0
**Dernière mise à jour**: 2026-03-31
**Licence**: Propriétaire

---

## 🚀 Déploiement sur Render

### Prérequis
- Compte Render gratuit : https://render.com
- Repository Git (GitHub, GitLab, ou Bitbucket)
- Clé API Ollama Cloud

### Étape 1 : Préparer le Repository

Assurez-vous que votre projet contient les fichiers suivants :
```
arcan-ai/
├── app.py                 # Serveur Flask
├── lesson_generator.py    # Logique de génération
├── index.html             # Interface utilisateur
├── requirements.txt       # Dépendances Python
├── Procfile               # Configuration Gunicorn
├── runtime.txt            # Version Python
├── .env.example           # Template de configuration
└── .gitignore             # Fichiers à ignorer
```

**Vérifiez que `.env` est dans `.gitignore`** :
```bash
cat .gitignore | grep .env
# Doit afficher: .env
```

### Étape 2 : Créer un Web Service sur Render

1. **Connectez-vous** à https://render.com
2. Cliquez sur **"New +"** → **"Web Service"**
3. **Connectez votre repository** :
   - Option A : Connectez GitHub/GitLab et sélectionnez votre repo
   - Option B : Utilisez "Public Git Repository" et collez l'URL

### Étape 3 : Configuration du Service

Remplissez les champs suivants :

| Champ | Valeur |
|-------|--------|
| **Name** | `arcan-ai` (ou nom de votre choix) |
| **Region** | Choisissez la plus proche de vos utilisateurs |
| **Branch** | `main` (ou votre branche principale) |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |

### Étape 4 : Variables d'environnement

Dans la section **"Environment Variables"**, ajoutez :

| Variable | Valeur | Description |
|----------|--------|-------------|
| `OLLAMA_API_KEY` | `votre_clé_api` | Clé API Ollama Cloud (obligatoire) |
| `OLLAMA_HOST` | `https://ollama.com` | URL de l'API Ollama |
| `DEFAULT_MODEL` | `gpt-oss:120b-cloud` | Modèle par défaut |
| `PORT` | `10000` | Render utilise le port 10000 par défaut |
| `FLASK_DEBUG` | `False` | Mode production |

**Comment ajouter les variables** :
1. Cliquez sur **"Add Environment Variable"**
2. Entrez le nom (ex: `OLLAMA_API_KEY`)
3. Entrez la valeur (votre clé API)
4. Répétez pour chaque variable

### Étape 5 : Déployer

1. Cliquez sur **"Create Web Service"**
2. Render va automatiquement :
   - Cloner votre repository
   - Installer les dépendances (`pip install -r requirements.txt`)
   - Démarrer l'application avec Gunicorn
3. Attendez le déploiement (2-5 minutes)

### Étape 6 : Vérifier le Déploiement

Une fois le déploiement terminé :

1. **Récupérez l'URL** de votre application (ex: `https://arcan-ai.onrender.com`)
2. **Testez l'endpoint de santé** :
   ```bash
   curl https://arcan-ai.onrender.com/api/health
   ```
   Réponse attendue :
   ```json
   {"status": "ok", "message": "Arcan-Ai opérationnel ✨"}
   ```

3. **Ouvrez l'interface** dans votre navigateur :
   ```
   https://arcan-ai.onrender.com
   ```

### Étape 7 : Configurer le Redémarrage Automatique

Render redémarre automatiquement l'application si elle plante. Pour un contrôle plus fin :

1. Allez dans **"Settings"** → **"Auto-Deploy"**
2. Activez **"Auto-Deploy"** pour redéployer automatiquement à chaque push

### Étape 8 : Surveiller les Logs

1. Allez dans l'onglet **"Logs"**
2. Surveillez les messages de démarrage :
   ```
   ============================================================
   🔮 Arcan-Ai — Tuteur Éducatif Personnalisé
   ============================================================
   🌐  URL     : http://localhost:10000
   📡  API     : http://localhost:10000/api/generate
   🔧  Mode    : Production
   ============================================================
   ```

### Dépannage Render

#### Erreur : "Build failed"
**Cause** : Problème d'installation des dépendances.
**Solution** :
1. Vérifiez que `requirements.txt` est correct
2. Vérifiez la version de Python dans `runtime.txt`
3. Consultez les logs de build

#### Erreur : "Application failed to respond"
**Cause** : L'application n'écoute pas sur le bon port.
**Solution** :
1. Vérifiez que `PORT` est défini dans les variables d'environnement
2. Assurez-vous que `app.py` utilise `os.environ.get('PORT', 5000)`
3. Vérifiez que Gunicorn est configuré pour écouter sur `0.0.0.0`

#### Erreur : "OLLAMA_API_KEY manquante"
**Cause** : Variable d'environnement non configurée.
**Solution** :
1. Allez dans **"Environment"**
2. Ajoutez `OLLAMA_API_KEY` avec votre clé API
3. Cliquez sur **"Save Changes"**
4. L'application redémarre automatiquement

#### Erreur : "Module not found"
**Cause** : Dépendance manquante dans `requirements.txt`.
**Solution** :
1. Vérifiez que toutes les dépendances sont listées
2. Ajoutez la dépendance manquante
3. Pushez les changements
4. Render redéploie automatiquement

### Optimisations Render

#### 1. Plan Gratuit vs Payant
| Fonctionnalité | Gratuit | Payant (Starter) |
|----------------|---------|------------------|
| Bande passante | 100 GB/mois | Illimité |
| RAM | 512 MB | 512 MB+ |
| CPU | Partagé | Dédié |
| Redémarrage | Après inactivité | Toujours actif |
| SSL | ✅ | ✅ |
| Domaine personnalisé | ✅ | ✅ |

#### 2. Éviter le "Cold Start"
Le plan gratuit met l'application en veille après 15 minutes d'inactivité. Pour éviter cela :
- Utilisez un service de monitoring (ex: UptimeRobot) pour ping l'application toutes les 5 minutes
- Ou passez au plan Starter (7$/mois)

#### 3. Variables d'Environnement Sécurisées
- Utilisez **"Secret Files"** pour les fichiers sensibles
- Ne commitez jamais `.env` dans votre repository
- Utilisez des variables d'environnement pour toutes les clés API

### Commandes Utiles Render

#### Via Dashboard
- **Redémarrer** : Settings → "Restart"
- **Voir les logs** : Onglet "Logs"
- **Modifier les variables** : Environment → "Add Environment Variable"
- **Forcer le déploiement** : Manual Deploy → "Deploy latest commit"

#### Via Render CLI (optionnel)
```bash
# Installer Render CLI
npm install -g render-cli

# Se connecter
render login

# Déployer
render deploy
```

### Checklist Déploiement Render

- [ ] Repository Git prêt avec tous les fichiers
- [ ] `.env` dans `.gitignore`
- [ ] `Procfile` configuré (`web: gunicorn app:app`)
- [ ] `runtime.txt` spécifie Python 3.11+
- [ ] `requirements.txt` complet
- [ ] Compte Render créé
- [ ] Web Service créé et configuré
- [ ] Variables d'environnement ajoutées
- [ ] Déploiement réussi
- [ ] Endpoint `/api/health` fonctionne
- [ ] Interface web accessible
- [ ] Génération de leçon testée

### URL de Votre Application

Une fois déployée, votre application sera accessible à :
```
https://arcan-ai.onrender.com
```

Partagez cette URL avec vos utilisateurs !

---

**🎉 Félicitations ! Votre application Arcan-Ai est maintenant déployée sur Render !**
