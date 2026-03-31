"""
Arcan-Ai — Pipeline de génération de leçons personnalisées.
Utilise l'API Ollama Cloud via la bibliothèque officielle.
"""
import os
import requests
from typing import List, Optional
from ollama import Client

# ─────────────────────────────────────────────────────────────
# Configuration — chargez votre clé via le fichier .env
# ─────────────────────────────────────────────────────────────
OLLAMA_API_KEY = os.environ.get('OLLAMA_API_KEY', '')
OLLAMA_HOST    = os.environ.get('OLLAMA_HOST', 'https://ollama.com')

DEFAULT_MODEL   = os.environ.get('DEFAULT_MODEL',   'gpt-oss:120b-cloud')
FINETUNED_MODEL = os.environ.get('FINETUNED_MODEL', 'gpt-oss:120b-cloud')

if not OLLAMA_API_KEY:
    raise EnvironmentError(
        "❌ Variable d'environnement OLLAMA_API_KEY manquante.\n"
        "   Créez un fichier .env à partir de .env.example et renseignez votre clé."
    )


# ─────────────────────────────────────────────────────────────
# Construction du prompt
# ─────────────────────────────────────────────────────────────
def build_prompt(
    subject: str,
    level: str,
    learning_style: str,
    topics: List[str],
    duration: Optional[int] = None
) -> str:
    """Construit le prompt de génération adapté au profil de l'élève."""

    topics_text   = ", ".join(topics) if topics else "général"
    duration_text = f"\nDurée de la session : {duration} minutes." if duration and duration > 0 else ""

    style_instructions = {
        "Visuel":          "Utilisez des diagrammes, schémas, cartes mentales et exemples visuels. Structurez clairement.",
        "Auditif":         "Expliquez avec des analogies, répétitions et exemples narratifs. Suggérez des mnémoniques.",
        "Kinesthésique":   "Proposez des exercices pratiques, expériences et manipulations interactives.",
        "Lecture/Écriture": "Fournissez des textes détaillés, des listes et des résumés. Encouragez la prise de notes.",
    }
    style_instruction = style_instructions.get(learning_style, style_instructions["Visuel"])

    return (
        f"Vous êtes un tuteur éducatif expert, spécialisé dans l'enseignement personnalisé. "
        f"Créez une leçon détaillée et engageante pour un élève de niveau {level} en {subject}. "
        f"Thèmes à couvrir : {topics_text}.{duration_text}\n\n"
        f"Style d'apprentissage de l'élève : {learning_style}\n"
        f"{style_instruction}\n\n"
        "La leçon doit inclure :\n"
        "📚 **Introduction** : Contextualiser le sujet et expliquer son importance\n"
        "🎯 **Objectifs d'apprentissage** : Ce que l'élève saura faire après la leçon\n"
        "📖 **Contenu principal** : Explications claires avec exemples concrets\n"
        "💡 **Exemples pratiques** : Applications réelles et exercices guidés\n"
        "✏️ **Exercices** : Questions de compréhension et problèmes à résoudre\n"
        "🎓 **Résumé** : Points clés à retenir\n"
        "🚀 **Pour aller plus loin** : Ressources et suggestions d'approfondissement\n\n"
        "Formatez la leçon de manière claire et structurée. "
        "Adaptez le vocabulaire et les exemples au niveau de l'élève. "
        "Rendez la leçon interactive et motivante."
    )


# ─────────────────────────────────────────────────────────────
# Génération de la leçon
# ─────────────────────────────────────────────────────────────
def generate_lesson(
    subject: str,
    level: str,
    learning_style: str,
    topics: List[str],
    duration: Optional[int] = None,
    model_name: Optional[str] = None
) -> str:
    """Génère une leçon personnalisée via l'API Ollama Cloud."""

    model_name = model_name or DEFAULT_MODEL
    prompt     = build_prompt(subject, level, learning_style, topics, duration)

    try:
        client = Client(
            host=OLLAMA_HOST,
            headers={'Authorization': f'Bearer {OLLAMA_API_KEY}'}
        )
        response = client.chat(
            model=model_name,
            messages=[{'role': 'user', 'content': prompt}],
            stream=False
        )
        return response['message']['content']

    except Exception as e:
        return f"❌ Erreur API Ollama : {str(e)}"


# ─────────────────────────────────────────────────────────────
# Test rapide en ligne de commande
# ─────────────────────────────────────────────────────────────
def main():
    subject        = "Mathématiques"
    level          = "Lycée"
    learning_style = "Visuel"
    topics         = ["Fonctions", "Dérivées"]
    duration       = 60

    print("=" * 80)
    print("🔮 Arcan-Ai — Tuteur Éducatif Personnalisé")
    print("=" * 80)
    print(f"Sujet          : {subject}")
    print(f"Niveau         : {level}")
    print(f"Style          : {learning_style}")
    print(f"Durée          : {duration} min")
    print(f"Thèmes         : {', '.join(topics)}")
    print("-" * 80)

    lesson = generate_lesson(
        subject=subject,
        level=level,
        learning_style=learning_style,
        topics=topics,
        duration=duration,
        model_name=DEFAULT_MODEL
    )
    print(lesson)
    print("-" * 80)


if __name__ == "__main__":
    main()
