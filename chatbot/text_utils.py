"""
chatbot/text_utils.py
Fonctions de traitement du texte et détection de langage.
"""

import re
import unicodedata
from typing import Optional

from rapidfuzz import fuzz
from spellchecker import SpellChecker

from chatbot.config import FUZZ_THRESHOLD

# Correction orthographique — instancié une seule fois
spell = SpellChecker()


def nettoyer_texte(texte: str) -> str:
    """Minuscules + suppression accents + suppression ponctuation."""
    texte = texte.lower()
    texte = unicodedata.normalize("NFD", texte)
    texte = texte.encode("ascii", "ignore").decode("utf-8")
    texte = re.sub(r"[^\w\s]", "", texte)
    return texte.strip()


def corriger_texte(texte: str) -> str:
    """Correction orthographique mot par mot."""
    mots = texte.split()
    mots_corriges = []
    for mot in mots:
        correction = spell.correction(mot)
        mots_corriges.append(correction if correction else mot)
    return " ".join(mots_corriges)


import re
from typing import Optional

from rapidfuzz import fuzz

from chatbot.config import FUZZ_THRESHOLD
from chatbot.text_utils import corriger_texte


def detecter_langage(texte: str, langages_disponibles: list) -> Optional[str]:
    """
    Détecte le langage de programmation mentionné dans le texte.
    Recherche par mots entiers pour éviter les faux positifs.
    """
    texte_corrige = corriger_texte(texte.lower())
    mots = re.findall(r"\b\w+\b", texte_corrige)  # découpe en mots
    for langage in langages_disponibles:
        if langage.lower() in mots:  # mot exact
            return langage
        # recherche floue uniquement si le mot a plus de 1 lettre
        if len(langage) > 1:
            score = fuzz.partial_ratio(langage.lower(), texte_corrige)
            if score > FUZZ_THRESHOLD:
                return langage
    return None
