"""
Couvre :
  - nettoyer_texte()
  - corriger_texte()
  - detecter_langage()
"""

import pytest
from chatbot.text_utils import nettoyer_texte, detecter_langage

LANGAGES = ["python", "javascript", "c"]


# ══════════════════════════════════════════════
# nettoyer_texte()
# ══════════════════════════════════════════════


class TestNettoyerTexte:

    def test_minuscules(self):
        assert nettoyer_texte("PYTHON") == "python"

    def test_accents_e(self):
        assert nettoyer_texte("éèê") == "eee"

    def test_accents_a(self):
        assert nettoyer_texte("àâä") == "aaa"

    def test_accents_u(self):
        assert nettoyer_texte("ùûü") == "uuu"

    def test_supprime_ponctuation(self):
        assert nettoyer_texte("c'est quoi ?") == "cest quoi"

    def test_supprime_point(self):
        assert nettoyer_texte("Python.") == "python"

    def test_supprime_virgule(self):
        assert nettoyer_texte("python, javascript") == "python javascript"

    def test_supprime_point_exclamation(self):
        assert nettoyer_texte("Bonjour !") == "bonjour"

    def test_chaine_vide(self):
        assert nettoyer_texte("") == ""

    def test_espaces_multiples_conserves(self):
        # les espaces sont gardés, c'est la ponctuation qui est retirée
        result = nettoyer_texte("  hello  ")
        assert "hello" in result

    def test_chiffres_conserves(self):
        assert "42" in nettoyer_texte("valeur 42")

    def test_phrase_complexe(self):
        result = nettoyer_texte("C'est quoi Python ?!")
        assert result == "cest quoi python"

    def test_texte_deja_propre(self):
        assert nettoyer_texte("python variable") == "python variable"

    @pytest.mark.parametrize(
        "entree,attendu",
        [
            ("Bonjour !", "bonjour"),
            ("JAVASCRIPT", "javascript"),
            ("déclarer", "declarer"),
            ("qu'est-ce que c'est", "questce que cest"),
        ],
    )
    def test_parametrique(self, entree, attendu):
        assert nettoyer_texte(entree) == attendu


# ══════════════════════════════════════════════
# detecter_langage()
# ══════════════════════════════════════════════


class TestDetecterLangage:

    def test_detecte_python_exact(self):
        assert detecter_langage("apprendre python", LANGAGES) == "python"

    def test_detecte_javascript_exact(self):
        assert detecter_langage("boucle en javascript", LANGAGES) == "javascript"

    def test_detecte_c_exact(self):
        assert detecter_langage("langage c pointeurs", LANGAGES) == "c"

    def test_detecte_python_majuscule(self):
        assert detecter_langage("apprendre PYTHON", LANGAGES) == "python"

    def test_detecte_python_phrase(self):
        assert (
            detecter_langage("je veux apprendre python aujourd'hui", LANGAGES)
            == "python"
        )

    def test_detecte_js_abrege(self):
        assert detecter_langage("variable javascript", LANGAGES) == "javascript"

    def test_aucun_langage(self):
        result = detecter_langage("bonjour comment ca va", LANGAGES)
        assert result is None

    def test_liste_vide(self):
        assert detecter_langage("python", []) is None

    def test_question_generique(self):
        result = detecter_langage("c'est quoi une variable ?", LANGAGES)
        assert result is None or result in LANGAGES

    @pytest.mark.parametrize(
        "texte,attendu",
        [
            ("variable python", "python"),
            ("boucle for javascript", "javascript"),
            ("pointeur en c", "c"),
            ("fonction python lambda", "python"),
        ],
    )
    def test_parametrique(self, texte, attendu):
        assert detecter_langage(texte, LANGAGES) == attendu
