"""Pipeline pour générer des leçons personnalisées avec Ollama Cloud API.
Ce fichier utilise l'API Ollama Cloud pour le déploiement.
"""
import os
import requests
from typing import List, Optional
from ollama import Client  # Utilise la bibliothèque officielle

# Configuration de l'API Ollama Cloud
OLLAMA_API_KEY = os.environ.get('OLLAMA_API_KEY', 'fc289982b86c43a8932b374295b7bd7b.fLzWxh3aqp2BQTPMo04iJzKT')
OLLAMA_HOST = "https://ollama.com"

# Nom du modèle par défaut
DEFAULT_MODEL = "gpt-oss:120b-cloud"  # Modèle disponible sur Ollama Cloud
FINETUNED_MODEL = "gpt-oss:120b-cloud"  # Changez si vous avez un modèle fine-tuné

# Vérifier si on utilise l'API Cloud ou local
USE_CLOUD_API = bool(OLLAMA_API_KEY and OLLAMA_API_KEY != 'your-api-key-here')


def build_prompt(subject: str, level: str, learning_style: str, topics: List[str], duration: Optional[int] = None) -> str:
    """Construit le prompt pour générer la leçon personnalisée.
    
    Args:
        subject: Le sujet d'étude (ex: Mathématiques, Français)
        level: Le niveau scolaire (ex: Primaire, Collège, Lycée)
        learning_style: Le style d'apprentissage préféré (Visuel, Auditif, Kinesthésique)
        topics: Liste des thèmes à couvrir
        duration: Durée de la session en minutes (optionnel)
        
    Returns:
        Le prompt formaté
    """
    topics_text = ", ".join(topics) if topics else "général"
    
    duration_text = ""
    if duration and duration > 0:
        duration_text = f"\nDurée de la session: {duration} minutes."
    
    # Adapter le prompt selon le style d'apprentissage
    style_instructions = {
        "Visuel": "Utilisez des diagrammes, schémas, cartes mentales et exemples visuels. Structurez clairement avec des couleurs et des icônes.",
        "Auditif": "Expliquez avec des analogies, répétitions et exemples narratifs. Suggérez des mnémoniques et des rythmes.",
        "Kinesthésique": "Proposez des exercices pratiques, des expériences et des manipulations. Incluez des activités interactives.",
        "Lecture/Écriture": "Fournissez des textes détaillés, des listes et des résumés écrits. Encouragez la prise de notes."
    }
    
    style_instruction = style_instructions.get(learning_style, style_instructions["Visuel"])
    
    return (
        f"Vous êtes un tuteur éducatif expert, spécialisé dans l'enseignement personnalisé. "
        f"Créez une leçon détaillée et engageante pour un élève de niveau {level} en {subject}. "
        f"Thèmes à couvrir: {topics_text}."
        f"{duration_text}\n\n"
        f"Style d'apprentissage de l'élève: {learning_style}\n"
        f"{style_instruction}\n\n"
        "La leçon doit inclure:\n"
        "📚 **Introduction**: Contextualiser le sujet et expliquer son importance\n"
        "🎯 **Objectifs d'apprentissage**: Ce que l'élève saura faire après la leçon\n"
        "📖 **Contenu principal**: Explications claires avec exemples concrets\n"
        "💡 **Exemples pratiques**: Applications réelles et exercices guidés\n"
        "✏️ **Exercices**: Questions de compréhension et problèmes à résoudre\n"
        "🎓 **Résumé**: Points clés à retenir\n"
        "🚀 **Pour aller plus loin**: Ressources et suggestions d'approfondissement\n\n"
        "Formatez la leçon de manière claire et structurée avec des sections bien définies. "
        "Adaptez le vocabulaire et les exemples au niveau de l'élève. "
        "Rendez la leçon interactive et motivante."
    )


def generate_lesson(
    subject: str, 
    level: str, 
    learning_style: str,
    topics: List[str],
    duration: Optional[int] = None,
    model_name: Optional[str] = None
) -> str:
    """Génère une leçon personnalisée en utilisant l'API Ollama Cloud.
    
    Args:
        subject: Le sujet d'étude
        level: Le niveau scolaire
        learning_style: Le style d'apprentissage
        topics: Liste des thèmes à couvrir
        duration: Durée de la session en minutes (optionnel)
        model_name: Le modèle à utiliser (optionnel)
        
    Returns:
        La leçon générée sous forme de texte
    """
    model_name = model_name or DEFAULT_MODEL
    prompt = build_prompt(subject, level, learning_style, topics, duration)
    
    try:
        # Initialisation du client comme dans la documentation
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
        return f"Erreur API: {str(e)}"


def main():
    """Fonction principale pour tester le générateur de leçons."""
    # Exemple d'utilisation
    subject = "Mathématiques"
    level = "Lycée"
    learning_style = "Visuel"
    topics = ["Fonctions", "Dérivées"]
    duration = 60
    
    print("=" * 80)
    print(f"📚 Tuteur Éducatif Personnalisé - Mode: {'Cloud API' if USE_CLOUD_API else 'Local'}")
    print("=" * 80)
    print(f"Sujet: {subject}")
    print(f"Niveau: {level}")
    print(f"Style d'apprentissage: {learning_style}")
    print(f"Durée: {duration} minutes")
    print(f"Thèmes: {', '.join(topics)}")
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