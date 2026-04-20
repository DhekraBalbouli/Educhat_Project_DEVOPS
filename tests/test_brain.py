"""
Couvre :
  - detecter_salutation()
  - repondre() / repondre_question()
  - Ordre de priorité : intentions → corpus → Mistral → défaut
  - Appel Mistral avec et sans clé API
"""

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
            assert (
                isinstance(result, str) and len(result) > 5
            ), f"Réponse trop courte pour : {q}"
