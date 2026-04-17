"""
chatbot/__init__.py
Exports publics du package.
main.py importe depuis ici — même interface qu'avant avec mon_chatbot.py.
"""

from chatbot.corpus    import data, langages_disponibles, repondre_question
from chatbot.text_utils import nettoyer_texte, detecter_langage
from chatbot.executor  import executer_et_capturer_sortie
from chatbot.quiz      import (
    get_quiz_questions, verifier_reponse_quiz,
    get_exercices_list, verifier_exercice,
    demarrer_quiz, demarrer_exercice,
)

# Salutations — identiques à mon_chatbot.py
salutations = {
    "bonjour": "Bonjour ! Comment puis-je t'aider à propos des langages de programmation ? 😊",
    "salut":   "Salut ! Pose-moi une question sur C, Python ou JavaScript.",
    "bonsoir": "Bonsoir ! Je suis là pour t'aider avec les langages de programmation.",
    "ca va":   "Je vais bien, merci ! Et toi ? Envie d'un quiz ou une explication ?",
}

__all__ = [
    "data",
    "langages_disponibles",
    "repondre_question",
    "nettoyer_texte",
    "detecter_langage",
    "executer_et_capturer_sortie",
    "salutations",
    "get_quiz_questions",
    "verifier_reponse_quiz",
    "get_exercices_list",
    "verifier_exercice",
    "demarrer_quiz",
    "demarrer_exercice",
]