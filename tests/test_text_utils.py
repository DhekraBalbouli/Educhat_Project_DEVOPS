import pytest
import allure
from chatbot.text_utils import nettoyer_texte, detecter_langage

LANGAGES = ["python", "javascript", "c"]


# ═══════════════════════════════════════
# NETTOYER TEXTE
# ═══════════════════════════════════════

@allure.feature("Nettoyage texte")
class TestNettoyerTexte:

    @allure.story("Minuscules")
    def test_minuscules(self):
        assert nettoyer_texte("PYTHON") == "python"

    @allure.story("Accents")
    def test_accents_e(self):
        assert nettoyer_texte("éèê") == "eee"

    @allure.story("Accents a")
    def test_accents_a(self):
        assert nettoyer_texte("àâä") == "aaa"

    @allure.story("Accents u")
    def test_accents_u(self):
        assert nettoyer_texte("ùûü") == "uuu"

    @allure.story("Ponctuation")
    def test_supprime_ponctuation(self):
        assert nettoyer_texte("c'est quoi ?") == "cest quoi"

    @allure.story("Point")
    def test_supprime_point(self):
        assert nettoyer_texte("Python.") == "python"

    @allure.story("Virgule")
    def test_supprime_virgule(self):
        assert nettoyer_texte("python, javascript") == "python javascript"

    @allure.story("Exclamation")
    def test_supprime_point_exclamation(self):
        assert nettoyer_texte("Bonjour !") == "bonjour"

    @allure.story("Chaine vide")
    def test_chaine_vide(self):
        assert nettoyer_texte("") == ""

    @allure.story("Texte simple")
    def test_texte_deja_propre(self):
        assert nettoyer_texte("python variable") == "python variable"

    @allure.story("Phrase complexe")
    def test_phrase_complexe(self):
        assert nettoyer_texte("C'est quoi Python ?!") == "cest quoi python"

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


# ═══════════════════════════════════════
# DETECTER LANGAGE
# ═══════════════════════════════════════

@allure.feature("Détection langage")
class TestDetecterLangage:

    @allure.story("Python exact")
    def test_detecte_python_exact(self):
        assert detecter_langage("apprendre python", LANGAGES) == "python"

    @allure.story("JavaScript exact")
    def test_detecte_javascript_exact(self):
        assert detecter_langage("boucle en javascript", LANGAGES) == "javascript"

    @allure.story("C exact")
    def test_detecte_c_exact(self):
        assert detecter_langage("langage c pointeurs", LANGAGES) == "c"

    @allure.story("Python majuscule")
    def test_detecte_python_majuscule(self):
        assert detecter_langage("PYTHON", LANGAGES) == "python"

    @allure.story("Phrase python")
    def test_detecte_python_phrase(self):
        assert detecter_langage("je veux apprendre python aujourd'hui", LANGAGES) == "python"

    @allure.story("Aucun langage")
    def test_aucun_langage(self):
        assert detecter_langage("bonjour comment ca va", LANGAGES) is None

    @allure.story("Liste vide")
    def test_liste_vide(self):
        assert detecter_langage("python", []) is None

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
