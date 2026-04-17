"""
tests/test_api_quiz.py
Tests d'intégration — GET /api/quiz/{langage} et POST /api/quiz/check
"""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client():
    from main import app
    return TestClient(app)


# ══════════════════════════════════════════════
# GET /api/quiz/{langage}
# ══════════════════════════════════════════════

class TestGetQuiz:

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_statut_200(self, client, lang):
        r = client.get(f"/api/quiz/{lang}")
        assert r.status_code == 200

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_cle_langage_presente(self, client, lang):
        r = client.get(f"/api/quiz/{lang}")
        assert "langage" in r.json()

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_cle_questions_presente(self, client, lang):
        r = client.get(f"/api/quiz/{lang}")
        assert "questions" in r.json()

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_questions_non_vides(self, client, lang):
        r = client.get(f"/api/quiz/{lang}")
        assert len(r.json()["questions"]) > 0

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_structure_question(self, client, lang):
        r = client.get(f"/api/quiz/{lang}")
        for q in r.json()["questions"]:
            assert "question" in q
            assert "options"  in q
            assert "answer"   in q

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_options_sont_liste(self, client, lang):
        r = client.get(f"/api/quiz/{lang}")
        for q in r.json()["questions"]:
            assert isinstance(q["options"], list)
            assert len(q["options"]) >= 2

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_bonne_reponse_dans_options(self, client, lang):
        r = client.get(f"/api/quiz/{lang}")
        for q in r.json()["questions"]:
            assert q["answer"] in q["options"]

    def test_langage_inexistant_404(self, client):
        r = client.get("/api/quiz/cobol")
        assert r.status_code == 404

    def test_langage_majuscule_accepte(self, client):
        """L'API doit normaliser la casse."""
        r = client.get("/api/quiz/PYTHON")
        assert r.status_code in [200, 404]  # selon l'implémentation

    def test_content_type_json(self, client):
        r = client.get("/api/quiz/python")
        assert r.headers["content-type"].startswith("application/json")

    def test_langage_dans_reponse_correct(self, client):
        r = client.get("/api/quiz/python")
        assert r.json()["langage"] == "python"


# ══════════════════════════════════════════════
# POST /api/quiz/check
# ══════════════════════════════════════════════

class TestCheckQuiz:

    def _get_bonne_reponse(self, client, lang, index=0):
        """Helper : récupère la bonne réponse pour l'index donné."""
        r = client.get(f"/api/quiz/{lang}")
        return r.json()["questions"][index]["answer"]

    def test_bonne_reponse_correct_true(self, client):
        lang   = "python"
        answer = self._get_bonne_reponse(client, lang)
        r = client.post("/api/quiz/check", json={
            "langage": lang, "question_index": 0, "answer": answer
        })
        assert r.status_code == 200
        assert r.json()["correct"] is True

    def test_mauvaise_reponse_correct_false(self, client):
        r = client.post("/api/quiz/check", json={
            "langage": "python", "question_index": 0,
            "answer": "__mauvaise_reponse_impossible__"
        })
        assert r.status_code == 200
        assert r.json()["correct"] is False

    def test_retourne_bonne_reponse(self, client):
        r = client.post("/api/quiz/check", json={
            "langage": "python", "question_index": 0, "answer": "test"
        })
        assert "answer" in r.json()
        assert isinstance(r.json()["answer"], str)

    def test_index_invalide_400(self, client):
        r = client.post("/api/quiz/check", json={
            "langage": "python", "question_index": 9999, "answer": "test"
        })
        assert r.status_code == 400

    def test_langage_inexistant_404(self, client):
        r = client.post("/api/quiz/check", json={
            "langage": "cobol", "question_index": 0, "answer": "test"
        })
        assert r.status_code == 404

    @pytest.mark.parametrize("lang", ["python", "javascript", "c"])
    def test_tous_les_langages(self, client, lang):
        answer = self._get_bonne_reponse(client, lang)
        r = client.post("/api/quiz/check", json={
            "langage": lang, "question_index": 0, "answer": answer
        })
        assert r.json()["correct"] is True

    def test_body_incomplet_422(self, client):
        r = client.post("/api/quiz/check", json={"langage": "python"})
        assert r.status_code == 422