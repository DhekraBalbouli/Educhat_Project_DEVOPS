"""
tests/test_api_langages.py
Tests d'intégration — GET /api/langages + GET /
"""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client():
    from main import app
    return TestClient(app)


# ══════════════════════════════════════════════
# GET /api/langages
# ══════════════════════════════════════════════

class TestGetLangages:

    def test_statut_200(self, client):
        r = client.get("/api/langages")
        assert r.status_code == 200

    def test_cle_langages_presente(self, client):
        r = client.get("/api/langages")
        assert "langages" in r.json()

    def test_langages_est_liste(self, client):
        r = client.get("/api/langages")
        assert isinstance(r.json()["langages"], list)

    def test_langages_non_vide(self, client):
        r = client.get("/api/langages")
        assert len(r.json()["langages"]) > 0

    def test_python_present(self, client):
        r = client.get("/api/langages")
        assert "python" in r.json()["langages"]

    def test_javascript_present(self, client):
        r = client.get("/api/langages")
        assert "javascript" in r.json()["langages"]

    def test_c_present(self, client):
        r = client.get("/api/langages")
        assert "c" in r.json()["langages"]

    def test_content_type_json(self, client):
        r = client.get("/api/langages")
        assert r.headers["content-type"].startswith("application/json")

    def test_coherence_avec_quiz(self, client):
        """Les langages de /api/langages doivent avoir des quiz disponibles."""
        langages = client.get("/api/langages").json()["langages"]
        for lang in langages:
            r = client.get(f"/api/quiz/{lang}")
            assert r.status_code == 200, f"Pas de quiz pour {lang}"

    def test_coherence_avec_exercices(self, client):
        """Les langages de /api/langages doivent avoir des exercices."""
        langages = client.get("/api/langages").json()["langages"]
        for lang in langages:
            r = client.get(f"/api/exercices/{lang}")
            assert r.status_code == 200, f"Pas d'exercices pour {lang}"


# ══════════════════════════════════════════════
# GET / (frontend)
# ══════════════════════════════════════════════

class TestRoot:

    def test_statut_200_ou_html(self, client):
        r = client.get("/")
        assert r.status_code == 200

    def test_retourne_html(self, client):
        r = client.get("/")
        assert "text/html" in r.headers["content-type"]

    def test_contenu_non_vide(self, client):
        r = client.get("/")
        assert len(r.text) > 0


# ══════════════════════════════════════════════
# Routes inexistantes
# ══════════════════════════════════════════════

class TestRoutesInexistantes:

    def test_route_inconnue_404(self, client):
        r = client.get("/api/inexistant")
        assert r.status_code == 404

    def test_methode_incorrecte_405(self, client):
        r = client.delete("/api/langages")
        assert r.status_code == 405