"""
Couvre :
  - get_quiz_questions()   : structure, options mélangées
  - verifier_reponse_quiz(): réponse correcte / incorrecte / index invalide
  - get_exercices_list()   : structure
  - verifier_exercice()    : code correct / code faux
"""

import pytest
from unittest.mock import patch, MagicMock
from chatbot.quiz import (
    get_quiz_questions,
    verifier_reponse_quiz,
    get_exercices_list,
    verifier_exercice,
)
from chatbot.corpus import data

# ══════════════════════════════════════════════
# get_quiz_questions()
# ══════════════════════════════════════════════


class TestGetQuizQuestions:

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_retourne_liste(self, lang):
        result = get_quiz_questions(lang)
        assert isinstance(result, list)

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_questions_non_vides(self, lang):
        result = get_quiz_questions(lang)
        assert len(result) > 0, f"Pas de questions pour {lang}"

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_structure_question(self, lang):
        questions = get_quiz_questions(lang)
        for q in questions:
            assert "question" in q
            assert "options" in q
            assert "answer" in q

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_options_sont_liste(self, lang):
        questions = get_quiz_questions(lang)
        for q in questions:
            assert isinstance(q["options"], list)
            assert len(q["options"]) >= 2

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_bonne_reponse_dans_options(self, lang):
        """La bonne réponse doit toujours être dans les options (même après shuffle)."""
        questions = get_quiz_questions(lang)
        for q in questions:
            assert (
                q["answer"] in q["options"]
            ), f"Réponse '{q['answer']}' absente des options pour {lang}"

    def test_options_melangees(self):
        """Appels multiples → ordre des options différent au moins une fois."""
        resultats = set()
        for _ in range(20):
            questions = get_quiz_questions("python")
            if questions:
                resultats.add(tuple(questions[0]["options"]))
        # Avec 4 options et 20 appels, on doit avoir au moins 2 ordres différents
        assert len(resultats) > 1, "Les options ne semblent pas être mélangées"


# ══════════════════════════════════════════════
# verifier_reponse_quiz()
# ══════════════════════════════════════════════


class TestVerifierReponseQuiz:

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_bonne_reponse(self, lang):
        questions_raw = data["langages"][lang]["quizzes"]
        for i, q in enumerate(questions_raw):
            result = verifier_reponse_quiz(lang, i, q["answer"])
            assert result["correct"] is True

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_mauvaise_reponse(self, lang):
        result = verifier_reponse_quiz(lang, 0, "__mauvaise_reponse_impossible__")
        assert result["correct"] is False

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_retourne_dict_avec_correct_et_answer(self, lang):
        result = verifier_reponse_quiz(lang, 0, "test")
        assert "correct" in result
        assert "answer" in result

    def test_insensible_casse(self):
        """La vérification doit être insensible à la casse."""
        lang = "python"
        q = data["langages"][lang]["quizzes"][0]
        # Réponse en majuscules
        result = verifier_reponse_quiz(lang, 0, q["answer"].upper())
        assert result["correct"] is True

    def test_avec_espaces(self):
        """Des espaces autour ne doivent pas invalider la réponse."""
        lang = "python"
        q = data["langages"][lang]["quizzes"][0]
        result = verifier_reponse_quiz(lang, 0, f"  {q['answer']}  ")
        assert result["correct"] is True

    def test_index_valide_premier(self):
        result = verifier_reponse_quiz("python", 0, "test")
        assert isinstance(result, dict)

    def test_index_invalide_leve_exception(self):
        with pytest.raises((IndexError, KeyError, Exception)):
            verifier_reponse_quiz("python", 9999, "test")


# ══════════════════════════════════════════════
# get_exercices_list()
# ══════════════════════════════════════════════


class TestGetExercicesList:

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_retourne_liste(self, lang):
        result = get_exercices_list(lang)
        assert isinstance(result, list)

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_exercices_non_vides(self, lang):
        result = get_exercices_list(lang)
        assert len(result) > 0

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_structure_exercice(self, lang):
        exercices = get_exercices_list(lang)
        for exo in exercices:
            assert "index" in exo
            assert "enonce" in exo

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_index_sequentiel(self, lang):
        exercices = get_exercices_list(lang)
        for i, exo in enumerate(exercices):
            assert exo["index"] == i

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_enonce_non_vide(self, lang):
        exercices = get_exercices_list(lang)
        for exo in exercices:
            assert len(exo["enonce"]) > 0

    def test_pas_de_solution_exposee(self):
        """La solution ne doit pas être exposée dans get_exercices_list."""
        for lang in ["python", "javascript", "c"]:
            exercices = get_exercices_list(lang)
            for exo in exercices:
                assert (
                    "solution" not in exo
                ), f"La solution est exposée pour {lang} — risque de triche !"


# ══════════════════════════════════════════════
# verifier_exercice()
# ══════════════════════════════════════════════


class TestVerifierExercice:

    def test_code_python_correct(self):
        """print('Hello World') doit matcher la solution 'Hello World'."""
        from chatbot.corpus import data as d

        # On prend le premier exercice Python et on crée le code correspondant
        solution = d["langages"]["python"]["exercices"][0]["solution"]
        code = f"print('{solution}')"
        result = verifier_exercice("python", 0, code)
        assert result["correct"] is True

    def test_code_python_incorrect(self):
        result = verifier_exercice("python", 0, "print('mauvaise_reponse_12345')")
        assert result["correct"] is False

    def test_retourne_output(self):
        result = verifier_exercice("python", 0, "print('test')")
        assert "output" in result
        assert "expected" in result
        assert "correct" in result

    def test_output_contient_sortie_reelle(self):
        result = verifier_exercice("python", 0, "print('Hello World')")
        assert isinstance(result["output"], str)

    def test_code_avec_erreur_syntaxe(self):
        result = verifier_exercice("python", 0, "print(")
        assert result["correct"] is False
        assert isinstance(result["output"], str)

    def test_index_invalide_leve_exception(self):
        with pytest.raises((IndexError, KeyError, Exception)):
            verifier_exercice("python", 9999, "print('test')")

    def test_verifier_exercice_js_mocke(self):
        mock_result = MagicMock()
        mock_result.stdout = "Hello\n"
        mock_result.stderr = ""
        with patch("subprocess.run", return_value=mock_result):
            result = verifier_exercice("javascript", 0, "console.log('Hello')")
        assert isinstance(result, dict)
        assert "correct" in result
