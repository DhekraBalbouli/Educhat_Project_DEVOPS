"""
chatbot/corpus.py
Chargement du fichier langages.yml + entraînement ChatterBot + indexation.
Code 100% identique à mon_chatbot.py — juste déplacé ici.
"""

import difflib
import random

import yaml
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

from chatbot.config import (CONFIDENCE_HIGH, CONFIDENCE_MID, DIFFLIB_CUTOFF,
                            RATIO_MIN, YAML_PATH)
from chatbot.text_utils import nettoyer_texte

# ── Chargement YAML ───────────────────────────────────────────────────────────
with open(YAML_PATH, "r", encoding="utf-8") as file:
    data = yaml.safe_load(file)

# ── ChatterBot ────────────────────────────────────────────────────────────────
chatbot = ChatBot("EduChat", read_only=False)
trainer = ListTrainer(chatbot)

# ── Indexation + Entraînement ─────────────────────────────────────────────────
questions_connues: list[str] = []
questions_indexees: dict[str, str] = {}

for langage, contenu in data["langages"].items():
    if "conversations" in contenu:
        for conv in contenu["conversations"]:
            if isinstance(conv, dict) and "question" in conv and "answers" in conv:
                # Entraînement ChatterBot (identique à mon_chatbot.py)
                trainer.train([conv["question"]] + conv["answers"])
                # Indexation pour difflib
                nettoyee = nettoyer_texte(conv["question"])
                questions_connues.append(nettoyee)
                questions_indexees[nettoyee] = conv["question"]

langages_disponibles: list[str] = list(data["langages"].keys())


def repondre_question(question: str) -> str:
    """
    Logique de réponse 100% identique à mon_chatbot.py :
      1. difflib get_close_matches
      2. SequenceMatcher ratio > 0.6
      3. ChatterBot avec niveaux de confiance
    """
    question_nettoyee = nettoyer_texte(question)
    correspondances = difflib.get_close_matches(
        question_nettoyee, questions_connues, n=3, cutoff=DIFFLIB_CUTOFF
    )

    if correspondances:
        for match in correspondances:
            question_originale = questions_indexees[match]
            for contenu in data["langages"].values():
                if "conversations" in contenu:
                    for conv in contenu["conversations"]:
                        if conv.get("question") == question_originale:
                            ratio = difflib.SequenceMatcher(
                                None,
                                question_nettoyee,
                                nettoyer_texte(question_originale),
                            ).ratio()
                            if ratio > RATIO_MIN:
                                return random.choice(conv["answers"])

    # Fallback ChatterBot (identique à mon_chatbot.py)
    reponse = chatbot.get_response(question)
    if reponse.confidence > CONFIDENCE_HIGH:
        return str(reponse)
    elif reponse.confidence > CONFIDENCE_MID:
        return f"Je pense que la réponse est: {reponse}, mais je ne suis pas totalement sûr."
    else:
        return "Je ne suis pas sûr d'avoir compris, peux-tu reformuler ?"
