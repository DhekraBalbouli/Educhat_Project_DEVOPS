"""
chatbot/__init__.py
Exports publics du package.
main.py importe depuis ici — même interface qu'avant avec mon_chatbot.py.
"""

from chatbot.corpus import data, langages_disponibles, repondre_question
from chatbot.executor import executer_et_capturer_sortie
from chatbot.quiz import (
    demarrer_exercice,
    demarrer_quiz,
    get_exercices_list,
    get_quiz_questions,
    verifier_exercice,
    verifier_reponse_quiz,
)
from chatbot.text_utils import detecter_langage, nettoyer_texte

# Salutations — identiques à mon_chatbot.py
salutations = {
    "bonjour": "Bonjour ! Comment puis-je t'aider à propos des langages ? 😊",
    "salut": "Salut ! Pose-moi une question sur C, Python ou JavaScript.",
    "bonsoir": "Bonsoir ! Je suis là pour t'aider avec les langages ",
    "ca va": "Je vais bien, merci ! Et toi  ?",
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
