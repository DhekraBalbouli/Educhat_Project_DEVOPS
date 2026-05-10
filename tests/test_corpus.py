"""
Couvre :
  - Chargement du fichier YAML
  - Structure des données
  - repondre_question() — logique de matching difflib + ChatterBot
  - langages_disponibles
"""

from unittest.mock import patch, MagicMock
# ══════════════════════════════════════════════
# Structure du corpus YAML
# ══════════════════════════════════════════════
class TestChargementCorpus:

    def test_data_charge(self):
        """Le fichier YAML est chargé correctement."""
        from chatbot.corpus import data

        assert data is not None
        assert isinstance(data, dict)

    def test_cle_langages_presente(self):
        from chatbot.corpus import data

        assert "langages" in data

    def test_langages_disponibles_non_vide(self):
        from chatbot.corpus import langages_disponibles

        assert len(langages_disponibles) > 0

    def test_python_present(self):
        from chatbot.corpus import data

        assert "python" in data["langages"]

    def test_javascript_present(self):
        from chatbot.corpus import data

        assert "javascript" in data["langages"]

    def test_c_present(self):
        from chatbot.corpus import data

        assert "c" in data["langages"]

    def test_chaque_langage_a_conversations(self):
        from chatbot.corpus import data

        for lang, contenu in data["langages"].items():
            assert "conversations" in contenu, f"Pas de conversations pour {lang}"

    def test_chaque_langage_a_quizzes(self):
        from chatbot.corpus import data

        for lang, contenu in data["langages"].items():
            assert "quizzes" in contenu, f"Pas de quizzes pour {lang}"

    def test_chaque_langage_a_exercices(self):
        from chatbot.corpus import data

        for lang, contenu in data["langages"].items():
            assert "exercices" in contenu, f"Pas d'exercices pour {lang}"

    def test_structure_conversation(self):
        """Chaque conversation a une question et des réponses."""
        from chatbot.corpus import data

        for lang, contenu in data["langages"].items():
            for conv in contenu["conversations"]:
                assert "question" in conv, f"Manque 'question' dans {lang}"
                assert "answers" in conv, f"Manque 'answers' dans {lang}"
                assert isinstance(conv["answers"], list)
                assert len(conv["answers"]) > 0

    def test_structure_quiz(self):
        """Chaque question de quiz a question, options et answer."""
        from chatbot.corpus import data
        for lang, contenu in data["langages"].items():
            for q in contenu["quizzes"]:
                assert "question" in q
                assert "options" in q
                assert "answer" in q
                assert isinstance(q["options"], list)
                assert len(q["options"]) >= 2
                assert (
                    q["answer"] in q["options"]
                ), f"La bonne réponse '{q['answer']}' n'est pas dans les options de {lang}"

    def test_structure_exercice(self):
        """Chaque exercice a un énoncé et une solution."""
        from chatbot.corpus import data
        for lang, contenu in data["langages"].items():
            for exo in contenu["exercices"]:
                assert "enonce" in exo
                assert "solution" in exo
                assert len(exo["enonce"]) > 0
                assert len(exo["solution"]) > 0


# ══════════════════════════════════════════════
# repondre_question() — matching
# ══════════════════════════════════════════════


class TestRepondreQuestion:

    def test_retourne_chaine(self):
        from chatbot.corpus import repondre_question
        result = repondre_question("python")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_question_tres_proche(self):
        """Une question très proche d'une entrée du corpus doit matcher."""
        from chatbot.corpus import repondre_question, data

        # On prend la première question du corpus et on la pose directement
        for lang, contenu in data["langages"].items():
            if contenu["conversations"]:
                question = contenu["conversations"][0]["question"]
                result = repondre_question(question)
                assert isinstance(result, str)
                assert len(result) > 0
                return

    def test_question_incomprehensible_ne_plante_pas(self):
        """Une question incompréhensible ne doit pas lever d'exception."""
        from chatbot.corpus import repondre_question

        result = repondre_question("xyzqwerty12345abcdef")
        assert isinstance(result, str)

    def test_question_vide_ne_plante_pas(self):
        from chatbot.corpus import repondre_question
        result = repondre_question("")
        assert isinstance(result, str)


    def test_question_longue_ne_plante_pas(self):
        from chatbot.corpus import repondre_question
        question = "comment faire " * 20 + "python"
        result = repondre_question(question)
        assert isinstance(result, str)
