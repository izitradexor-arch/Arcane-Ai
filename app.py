"""
Arcan-Ai — Serveur Flask
Fait le pont entre le frontend et l'API Ollama Cloud.
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os
from dotenv import load_dotenv

# Charger les variables d'environnement AVANT tout import du générateur
load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from lesson_generator import generate_lesson, DEFAULT_MODEL, FINETUNED_MODEL
except EnvironmentError as env_err:
    print(f"\n{'='*60}")
    print(str(env_err))
    print(f"{'='*60}\n")
    sys.exit(1)
except ImportError:
    def generate_lesson(subject, level, learning_style, topics=None, duration=None, model_name=None):
        return "Erreur : lesson_generator.py introuvable. Placez-le dans le même dossier que app.py."
    DEFAULT_MODEL   = "gpt-oss:120b-cloud"
    FINETUNED_MODEL = "gpt-oss:120b-cloud"


app = Flask(__name__, static_folder='.')

CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],          # Remplacez par votre domaine en production
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})


# ─────────────────────────────────────────────────────────────
# Routes statiques
# ─────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


# ─────────────────────────────────────────────────────────────
# API — Génération de leçon
# ─────────────────────────────────────────────────────────────
@app.route('/api/generate', methods=['POST'])
def generate():
    """
    Génère une leçon personnalisée.

    Body JSON attendu :
    {
        "subject":        "Mathématiques",
        "level":          "Lycée",
        "learning_style": "Visuel",
        "topics":         ["Algèbre", "Géométrie"],
        "duration":       60,            // optionnel, 15-180 min
        "model":          "gpt-oss:120b-cloud"  // optionnel
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Aucune donnée fournie"}), 400

        subject        = data.get('subject',        '').strip()
        level          = data.get('level',          '').strip()
        learning_style = data.get('learning_style', '').strip()
        topics         = data.get('topics',         [])
        duration       = data.get('duration')
        model_name     = data.get('model', DEFAULT_MODEL)

        # Validation des champs obligatoires
        if not subject:
            return jsonify({"error": "Le sujet est requis"}), 400
        if not level:
            return jsonify({"error": "Le niveau est requis"}), 400
        if not learning_style:
            return jsonify({"error": "Le style d'apprentissage est requis"}), 400
        if not isinstance(topics, list) or len(topics) == 0:
            return jsonify({"error": "Veuillez sélectionner au moins un thème"}), 400

        # Validation de la durée (optionnelle)
        if duration is not None:
            try:
                duration = int(duration)
                if not (15 <= duration <= 180):
                    return jsonify({"error": "La durée doit être entre 15 et 180 minutes"}), 400
            except (TypeError, ValueError):
                return jsonify({"error": "La durée doit être un nombre valide"}), 400

        print(f"[Arcan-Ai] Génération → {subject} | {level} | {learning_style} | {duration}min | {topics}")

        lesson = generate_lesson(
            subject=subject,
            level=level,
            learning_style=learning_style,
            topics=topics,
            duration=duration,
            model_name=model_name
        )

        return jsonify({
            "success":        True,
            "lesson":         lesson,
            "subject":        subject,
            "level":          level,
            "learning_style": learning_style,
            "topics":         topics,
            "duration":       duration
        })

    except Exception as e:
        print(f"[Arcan-Ai] Erreur : {str(e)}")
        return jsonify({"success": False, "error": f"Erreur lors de la génération : {str(e)}"}), 500


# ─────────────────────────────────────────────────────────────
# API — Modèles disponibles (uniquement Cloud)
# ─────────────────────────────────────────────────────────────
@app.route('/api/models', methods=['GET'])
def get_models():
    return jsonify({
        "models":  [DEFAULT_MODEL, FINETUNED_MODEL],
        "default": DEFAULT_MODEL
    })


# ─────────────────────────────────────────────────────────────
# API — Santé
# ─────────────────────────────────────────────────────────────
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "message": "Arcan-Ai opérationnel ✨"})


# ─────────────────────────────────────────────────────────────
# Démarrage
# ─────────────────────────────────────────────────────────────
if __name__ == '__main__':
    port  = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

    print("=" * 60)
    print("🔮 Arcan-Ai — Tuteur Éducatif Personnalisé")
    print("=" * 60)
    print(f"🌐  URL     : http://localhost:{port}")
    print(f"📡  API     : http://localhost:{port}/api/generate")
    print(f"🔧  Mode    : {'Debug' if debug else 'Production'}")
    print("=" * 60)

    app.run(debug=debug, host='0.0.0.0', port=port)
