"""
API Flask pour le tuteur éducatif personnalisé.
Ce backend fait le pont entre le frontend et Ollama Cloud API.
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Ajouter le chemin du module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from itinerary_generator2 import generate_lesson, DEFAULT_MODEL, FINETUNED_MODEL
except ImportError:
    # Fallback si tutor_generator.py n'est pas trouvé
    def generate_lesson(subject, level, learning_style, topics=None, duration=None, model_name=None):
        return "Erreur: Le fichier tutor_generator.py n'a pas été trouvé. Assurez-vous qu'il est dans le même dossier que app.py"
    DEFAULT_MODEL = "gpt-oss:120b-cloud"
    FINETUNED_MODEL = "gpt-oss:120b-cloud"

app = Flask(__name__, static_folder='static')

# Configuration CORS pour le déploiement
CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],  # En production, remplacez par votre domaine
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route('/')
def index():
    """Servir la page d'accueil."""
    return send_from_directory('static', 'index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    """
    Endpoint pour générer une leçon personnalisée.
    
    Expects JSON:
    {
        "subject": "Mathématiques",
        "level": "Lycée",
        "learning_style": "Visuel",
        "topics": ["Algèbre", "Géométrie"],
        "duration": 60,
        "model": "gpt-oss:120b-cloud" (optional)
    }
    """
    try:
        data = request.get_json()
        
        # Validation des données
        if not data:
            return jsonify({"error": "Aucune donnée fournie"}), 400
        
        subject = data.get('subject', '').strip()
        level = data.get('level', '').strip()
        learning_style = data.get('learning_style', '').strip()
        topics = data.get('topics', [])
        duration = data.get('duration')
        model_name = data.get('model', DEFAULT_MODEL)
        
        # Validation
        if not subject:
            return jsonify({"error": "Le sujet est requis"}), 400
        
        if not level:
            return jsonify({"error": "Le niveau est requis"}), 400
        
        if not learning_style:
            return jsonify({"error": "Le style d'apprentissage est requis"}), 400
        
        if not isinstance(topics, list) or len(topics) == 0:
            return jsonify({"error": "Veuillez sélectionner au moins un thème"}), 400
        
        # Validation de la durée (optionnel)
        if duration is not None:
            try:
                duration = int(duration)
                if duration < 15 or duration > 180:
                    return jsonify({"error": "La durée doit être entre 15 et 180 minutes"}), 400
            except (TypeError, ValueError):
                return jsonify({"error": "La durée doit être un nombre valide"}), 400
        
        # Générer la leçon
        print(f"Génération de leçon pour {subject}, niveau {level}, style: {learning_style}, durée: {duration}min, thèmes: {topics}")
        lesson = generate_lesson(
            subject=subject,
            level=level,
            learning_style=learning_style,
            topics=topics,
            duration=duration,
            model_name=model_name
        )
        
        return jsonify({
            "success": True,
            "lesson": lesson,
            "subject": subject,
            "level": level,
            "learning_style": learning_style,
            "topics": topics,
            "duration": duration
        })
        
    except Exception as e:
        print(f"Erreur lors de la génération: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Erreur lors de la génération: {str(e)}"
        }), 500

@app.route('/api/models', methods=['GET'])
def get_models():
    """Retourner la liste des modèles disponibles."""
    return jsonify({
        "models": [
            DEFAULT_MODEL,
            FINETUNED_MODEL,
            "llama2:7b",
            "gemma:7b"
        ],
        "default": DEFAULT_MODEL
    })

@app.route('/api/health', methods=['GET'])
def health():
    """Vérifier l'état de l'API."""
    return jsonify({
        "status": "ok",
        "message": "API du tuteur éducatif opérationnelle"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print("=" * 60)
    print("📚 Serveur de tuteur éducatif personnalisé démarré")
    print("=" * 60)
    print(f"🌐 URL: http://localhost:{port}")
    print(f"📡 API: http://localhost:{port}/api/generate")
    print(f"🔧 Mode: {'Debug' if debug else 'Production'}")
    print("=" * 60)
    
    app.run(debug=debug, host='0.0.0.0', port=port)