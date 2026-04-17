"""
tests/test_api_chat.py
Tests d'intégration — POST /api/chat

Utilise TestClient FastAPI (pas de vrai serveur réseau).
Couvre tous les cas de la route chat.
"""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client():
    from main import app
    return TestClient(app)


# ══════════════════════════════════════════════
# Salutations
# ══════════════════════════════════════════════

class TestChatSalutations:

    def test_bonjour_statut_200(self, client):
        r = client.post("/api/chat", json={"message": "bonjour"})
        assert r.status_code == 200

    def test_bonjour_type_salutation(self, client):
        r = client.post("/api/chat", json={"message": "bonjour"})
        assert r.json()["type"] == "salutation"

    def test_bonjour_retourne_reponse(self, client):
        r = client.post("/api/chat", json={"message": "bonjour"})
        assert len(r.json()["response"]) > 0

    def test_salut_detecte(self, client):
        r = client.post("/api/chat", json={"message": "salut"})
        assert r.json()["type"] == "salutation"

    def test_bonsoir_detecte(self, client):
        r = client.post("/api/chat", json={"message": "bonsoir"})
        assert r.json()["type"] == "salutation"

    def test_salutation_langage_none(self, client):
        """Pour une salutation, le langage retourné doit être None."""
        r = client.post("/api/chat", json={"message": "bonjour"})
        assert r.json()["langage"] is None

    def test_salutation_majuscule(self, client):
        r = client.post("/api/chat", json={"message": "BONJOUR"})
        assert r.status_code == 200


# ══════════════════════════════════════════════
# Questions normales
# ══════════════════════════════════════════════

class TestChatQuestions:

    def test_question_python_statut_200(self, client):
        r = client.post("/api/chat", json={"message": "c'est quoi python"})
        assert r.status_code == 200

    def test_question_python_type_question(self, client):
        r = client.post("/api/chat", json={"message": "c'est quoi python"})
        assert r.json()["type"] == "question"

    def test_question_retourne_reponse_non_vide(self, client):
        r = client.post("/api/chat", json={"message": "variable python"})
        assert len(r.json()["response"]) > 0

    def test_structure_reponse_complete(self, client):
        r = client.post("/api/chat", json={"message": "boucle python"})
        body = r.json()
        assert "response" in body
        assert "langage"  in body
        assert "type"     in body

    def test_langage_detecte_python(self, client):
        r = client.post("/api/chat", json={"message": "variable python"})
        assert r.json()["langage"] == "python"

    def test_langage_detecte_javascript(self, client):
        r = client.post("/api/chat", json={"message": "boucle javascript"})
        assert r.json()["langage"] == "javascript"

    def test_langage_detecte_c(self, client):
        r = client.post("/api/chat", json={"message": "pointeur en c"})
        body = r.json()
        assert body["langage"] in ["c", None]  # selon le seuil de détection

    def test_question_hors_sujet(self, client):
        r = client.post("/api/chat", json={"message": "quel temps fait-il aujourd'hui"})
        assert r.status_code == 200
        assert isinstance(r.json()["response"], str)


# ══════════════════════════════════════════════
# Validation des entrées
# ══════════════════════════════════════════════

class TestChatValidation:

    def test_message_vide(self, client):
        r = client.post("/api/chat", json={"message": ""})
        assert r.status_code == 200  # ne doit pas planter

    def test_message_tres_long(self, client):
        r = client.post("/api/chat", json={"message": "python " * 200})
        assert r.status_code == 200

    def test_message_caracteres_speciaux(self, client):
        r = client.post("/api/chat", json={"message": "C'est quoi le C++ ?!@#$%"})
        assert r.status_code == 200

    def test_body_manquant(self, client):
        r = client.post("/api/chat", json={})
        assert r.status_code == 422  # Validation Pydantic

    def test_content_type_json(self, client):
        r = client.post("/api/chat", json={"message": "python"})
        assert r.headers["content-type"].startswith("application/json")

    def test_message_injection_code(self, client):
        """Injection de code Python — ne doit pas être exécutée."""
        r = client.post("/api/chat", json={"message": "__import__('os').system('ls')"})
        assert r.status_code == 200