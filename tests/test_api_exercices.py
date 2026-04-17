"""
tests/test_api_exercices.py
Tests d'intégration — GET /api/exercices/{langage} et POST /api/exercices/check
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client():
    from main import app
    return TestClient(app)


# ══════════════════════════════════════════════
# GET /api/exercices/{langage}
# ══════════════════════════════════════════════

class TestGetExercices:

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_statut_200(self, client, lang):
        r = client.get(f"/api/exercices/{lang}")
        assert r.status_code == 200

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_cle_langage_presente(self, client, lang):
        r = client.get(f"/api/exercices/{lang}")
        assert "langage" in r.json()

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_cle_exercices_presente(self, client, lang):
        r = client.get(f"/api/exercices/{lang}")
        assert "exercices" in r.json()

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_exercices_non_vides(self, client, lang):
        r = client.get(f"/api/exercices/{lang}")
        assert len(r.json()["exercices"]) > 0

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_structure_exercice(self, client, lang):
        r = client.get(f"/api/exercices/{lang}")
        for exo in r.json()["exercices"]:
            assert "index"  in exo
            assert "enonce" in exo

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_pas_de_solution_exposee(self, client, lang):
        """La solution ne doit JAMAIS être exposée dans la réponse GET."""
        r = client.get(f"/api/exercices/{lang}")
        for exo in r.json()["exercices"]:
            assert "solution" not in exo, \
                f"SECURITE : solution exposee pour {lang} exercice {exo['index']}"

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_index_sequentiel(self, client, lang):
        r = client.get(f"/api/exercices/{lang}")
        for i, exo in enumerate(r.json()["exercices"]):
            assert exo["index"] == i

    def test_langage_inexistant_404(self, client):
        r = client.get("/api/exercices/cobol")
        assert r.status_code == 404


# ══════════════════════════════════════════════
# POST /api/exercices/check
# ══════════════════════════════════════════════

class TestCheckExercice:

    def test_code_python_correct(self, client):
        """Code qui produit la bonne sortie → correct=True."""
        # D'abord récupérer l'énoncé pour savoir ce qu'on attend
        r_exos = client.get("/api/exercices/python")
        solution_attendue = None
        # On récupère la solution depuis le corpus directement
        from chatbot.corpus import data
        solution_attendue = data["langages"]["python"]["exercices"][0]["solution"]

        r = client.post("/api/exercices/check", json={
            "code": f"print('{solution_attendue}')",
            "langage": "python",
            "exercice_index": 0
        })
        assert r.status_code == 200
        assert r.json()["correct"] is True

    def test_code_python_incorrect(self, client):
        r = client.post("/api/exercices/check", json={
            "code": "print('sortie_completement_fausse_xyzqwerty')",
            "langage": "python",
            "exercice_index": 0
        })
        assert r.status_code == 200
        assert r.json()["correct"] is False

    def test_retourne_output(self, client):
        r = client.post("/api/exercices/check", json={
            "code": "print('test')",
            "langage": "python",
            "exercice_index": 0
        })
        assert "output"   in r.json()
        assert "expected" in r.json()
        assert "correct"  in r.json()

    def test_output_est_chaine(self, client):
        r = client.post("/api/exercices/check", json={
            "code": "print('hello')",
            "langage": "python",
            "exercice_index": 0
        })
        assert isinstance(r.json()["output"], str)

    def test_expected_est_chaine(self, client):
        r = client.post("/api/exercices/check", json={
            "code": "print('test')",
            "langage": "python",
            "exercice_index": 0
        })
        assert isinstance(r.json()["expected"], str)

    def test_index_invalide_400(self, client):
        r = client.post("/api/exercices/check", json={
            "code": "print('test')",
            "langage": "python",
            "exercice_index": 9999
        })
        assert r.status_code == 400

    def test_langage_inexistant_404(self, client):
        r = client.post("/api/exercices/check", json={
            "code": "print('test')",
            "langage": "cobol",
            "exercice_index": 0
        })
        assert r.status_code == 404

    def test_code_erreur_syntaxe_ne_plante_pas(self, client):
        r = client.post("/api/exercices/check", json={
            "code": "print(",
            "langage": "python",
            "exercice_index": 0
        })
        assert r.status_code == 200
        assert r.json()["correct"] is False

    def test_code_vide(self, client):
        r = client.post("/api/exercices/check", json={
            "code": "",
            "langage": "python",
            "exercice_index": 0
        })
        assert r.status_code == 200

    def test_body_incomplet_422(self, client):
        r = client.post("/api/exercices/check", json={"langage": "python"})
        assert r.status_code == 422

    def test_exercice_js_mocke(self, client):
        mock_result = MagicMock()
        mock_result.stdout = "Hello\n"
        mock_result.stderr = ""
        with patch("subprocess.run", return_value=mock_result):
            r = client.post("/api/exercices/check", json={
                "code": "console.log('Hello')",
                "langage": "javascript",
                "exercice_index": 0
            })
        assert r.status_code == 200
        assert "correct" in r.json()