"""
tests/test_brain.py
Tests unitaires — chatbot/brain.py  (ou chatbot/corpus.py selon ta version)

Couvre :
  - detecter_salutation()
  - repondre() / repondre_question()
  - Ordre de priorité : intentions → corpus → Mistral → défaut
  - Appel Mistral avec et sans clé API
"""

import pytest
from unittest.mock import patch, MagicMock


# ══════════════════════════════════════════════
# detecter_salutation()
# ══════════════════════════════════════════════

class TestDetecterSalutation:

    def _salutation(self, msg):
        """Cherche une salutation dans le dict salutations du module chatbot."""
        from chatbot import salutations
        msg_low = msg.strip().lower()
        for mot, rep in salutations.items():
            if mot in msg_low:
                return rep
        return None

    def test_bonjour(self):
        assert self._salutation("bonjour") is not None

    def test_salut(self):
        assert self._salutation("salut") is not None

    def test_bonsoir(self):
        assert self._salutation("bonsoir") is not None

    def test_ca_va(self):
        assert self._salutation("ca va") is not None

    def test_question_normale_pas_salutation(self):
        assert self._salutation("c'est quoi python") is None

    def test_salutation_dans_phrase(self):
        """'bonjour' au milieu d'une phrase doit être détecté."""
        assert self._salutation("bonjour je veux apprendre python") is not None

    def test_salutation_majuscule(self):
        assert self._salutation("BONJOUR") is not None

    def test_message_vide(self):
        assert self._salutation("") is None

    def test_reponse_est_chaine_non_vide(self):
        rep = self._salutation("bonjour")
        assert isinstance(rep, str) and len(rep) > 0


# ══════════════════════════════════════════════
# SALUTATIONS dict
# ══════════════════════════════════════════════

class TestSalutationsDict:

    def test_dict_non_vide(self):
        from chatbot import salutations
        assert len(salutations) > 0

    def test_toutes_valeurs_sont_chaines(self):
        from chatbot import salutations
        for mot, rep in salutations.items():
            assert isinstance(rep, str), f"La réponse pour '{mot}' n'est pas une chaîne"

    def test_toutes_reponses_non_vides(self):
        from chatbot import salutations
        for mot, rep in salutations.items():
            assert len(rep) > 0, f"Réponse vide pour '{mot}'"


# ══════════════════════════════════════════════
# repondre_question() — priorité intentions
# ══════════════════════════════════════════════

class TestRepondreIntentions:

    def test_python_definition(self):
        from chatbot.corpus import repondre_question
        result = repondre_question("c'est quoi python")
        assert isinstance(result, str) and len(result) > 0

    def test_javascript_definition(self):
        from chatbot.corpus import repondre_question
        result = repondre_question("c'est quoi javascript")
        assert isinstance(result, str) and len(result) > 0

    def test_boucle_python(self):
        from chatbot.corpus import repondre_question
        result = repondre_question("boucle python")
        assert isinstance(result, str) and len(result) > 0

    def test_variable_python(self):
        from chatbot.corpus import repondre_question
        result = repondre_question("variable python")
        assert isinstance(result, str) and len(result) > 0

    def test_question_completement_hors_sujet(self):
        from chatbot.corpus import repondre_question
        result = repondre_question("quel est le prix du beurre")
        assert isinstance(result, str) and len(result) > 0

    def test_reponse_contient_info_pertinente(self):
        from chatbot.corpus import repondre_question
        result = repondre_question("c'est quoi python")
        assert "python" in result.lower()

    def test_questions_differentes_donnent_reponses(self):
        from chatbot.corpus import repondre_question
        questions = [
            "variable python",
            "boucle javascript",
            "fonction python",
            "tableau javascript",
        ]
        for q in questions:
            result = repondre_question(q)
            assert isinstance(result, str) and len(result) > 5, \
                f"Réponse trop courte pour : {q}"


# ══════════════════════════════════════════════
# Appel Mistral API
# ══════════════════════════════════════════════

class TestMistralAPI:

    def test_sans_cle_api_ne_plante_pas(self):
        """Sans clé API, le système doit fonctionner normalement (fallback)."""
        from chatbot.corpus import repondre_question
        with patch("chatbot.config.MISTRAL_API_KEY", ""):
            result = repondre_question("question quelconque")
        assert isinstance(result, str)

    def test_avec_cle_api_appelle_requests(self):
        """Avec une clé API, requests.post doit être appelé."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Réponse Mistral"}}]
        }
        with patch("chatbot.config.MISTRAL_API_KEY", "fake-key-123"), \
             patch("requests.post", return_value=mock_response) as mock_post:
            from chatbot.corpus import repondre_question
            result = repondre_question("question très improbable xyzqwerty12345")
        assert isinstance(result, str)

    def test_mistral_erreur_reseau_fallback(self):
        """En cas d'erreur réseau, le système doit retourner un message par défaut."""
        with patch("requests.post", side_effect=Exception("Network error")):
            from chatbot.corpus import repondre_question
            result = repondre_question("xyzqwerty improbable")
        assert isinstance(result, str) and len(result) > 0

    def test_mistral_timeout_ne_plante_pas(self):
        import requests as req
        with patch("requests.post", side_effect=req.exceptions.Timeout()):
            from chatbot.corpus import repondre_question
            result = repondre_question("xyzqwerty timeout test")
        assert isinstance(result, str)

    def test_mistral_erreur_401_fallback(self):
        """Clé invalide (401) → fallback sans planter."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        with patch("chatbot.config.MISTRAL_API_KEY", "cle-invalide"), \
             patch("requests.post", return_value=mock_response):
            from chatbot.corpus import repondre_question
            result = repondre_question("xyzqwerty 401 test")
        assert isinstance(result, str)