"""
tests/test_api_execute.py
Tests d'intégration — POST /api/execute  (bac à sable)
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client():
    from main import app
    return TestClient(app)


# ══════════════════════════════════════════════
# Python — cas normaux
# ══════════════════════════════════════════════

class TestExecutePython:

    def test_hello_world_statut_200(self, client):
        r = client.post("/api/execute", json={"code": "print('Hello')", "langage": "python"})
        assert r.status_code == 200

    def test_hello_world_sortie(self, client):
        r = client.post("/api/execute", json={"code": "print('Hello')", "langage": "python"})
        assert r.json()["output"] == "Hello"

    def test_calcul_python(self, client):
        r = client.post("/api/execute", json={"code": "print(2 + 2)", "langage": "python"})
        assert r.json()["output"] == "4"

    def test_variable_print(self, client):
        r = client.post("/api/execute", json={
            "code": "x = 10\nprint(x)", "langage": "python"
        })
        assert r.json()["output"] == "10"

    def test_boucle_for(self, client):
        r = client.post("/api/execute", json={
            "code": "for i in range(3):\n    print(i)", "langage": "python"
        })
        assert "0" in r.json()["output"]

    def test_structure_reponse(self, client):
        r = client.post("/api/execute", json={"code": "print('ok')", "langage": "python"})
        body = r.json()
        assert "output"  in body
        assert "langage" in body

    def test_langage_retourne_dans_reponse(self, client):
        r = client.post("/api/execute", json={"code": "print('ok')", "langage": "python"})
        assert r.json()["langage"] == "python"

    def test_erreur_syntaxe_pas_500(self, client):
        r = client.post("/api/execute", json={"code": "print(", "langage": "python"})
        assert r.status_code == 200  # L'erreur est dans output, pas en HTTP 500
        assert "erreur" in r.json()["output"].lower() or "error" in r.json()["output"].lower()

    def test_erreur_runtime_pas_500(self, client):
        r = client.post("/api/execute", json={"code": "print(1/0)", "langage": "python"})
        assert r.status_code == 200
        assert "erreur" in r.json()["output"].lower() or "ZeroDivision" in r.json()["output"]

    def test_code_sans_sortie(self, client):
        r = client.post("/api/execute", json={"code": "x = 42", "langage": "python"})
        assert r.status_code == 200
        output = r.json()["output"]
        assert "aucune" in output.lower() or output == ""


# ══════════════════════════════════════════════
# JavaScript (mocké)
# ══════════════════════════════════════════════

class TestExecuteJavaScript:

    def test_hello_js_mocke(self, client):
        mock_result = MagicMock()
        mock_result.stdout = "Hello JS\n"
        mock_result.stderr = ""
        with patch("subprocess.run", return_value=mock_result):
            r = client.post("/api/execute", json={
                "code": "console.log('Hello JS')", "langage": "javascript"
            })
        assert r.status_code == 200
        assert "Hello JS" in r.json()["output"]

    def test_erreur_js_mocke(self, client):
        mock_result = MagicMock()
        mock_result.stdout = ""
        mock_result.stderr = "ReferenceError: x is not defined"
        with patch("subprocess.run", return_value=mock_result):
            r = client.post("/api/execute", json={
                "code": "console.log(x)", "langage": "javascript"
            })
        assert r.status_code == 200
        output = r.json()["output"]
        assert "erreur" in output.lower() or "Error" in output

    def test_langage_js_dans_reponse(self, client):
        mock_result = MagicMock()
        mock_result.stdout = "ok\n"
        mock_result.stderr = ""
        with patch("subprocess.run", return_value=mock_result):
            r = client.post("/api/execute", json={
                "code": "console.log('ok')", "langage": "javascript"
            })
        assert r.json()["langage"] == "javascript"


# ══════════════════════════════════════════════
# C (mocké)
# ══════════════════════════════════════════════

class TestExecuteC:

    def test_hello_c_mocke(self, client):
        compile_mock = MagicMock(returncode=0, stderr="")
        exec_mock    = MagicMock(stdout="Hello C\n", stderr="")
        with patch("subprocess.run", side_effect=[compile_mock, exec_mock]):
            r = client.post("/api/execute", json={
                "code": '#include<stdio.h>\nint main(){printf("Hello C");return 0;}',
                "langage": "c"
            })
        assert r.status_code == 200
        assert "Hello C" in r.json()["output"]

    def test_erreur_compilation_c(self, client):
        compile_mock = MagicMock(returncode=1, stderr="error: missing semicolon")
        with patch("subprocess.run", return_value=compile_mock):
            r = client.post("/api/execute", json={
                "code": "int main(){return 0", "langage": "c"
            })
        assert r.status_code == 200
        output = r.json()["output"]
        assert "erreur" in output.lower() or "error" in output.lower()


# ══════════════════════════════════════════════
# Langage non supporté + validation
# ══════════════════════════════════════════════

class TestExecuteValidation:

    def test_langage_inconnu_pas_500(self, client):
        r = client.post("/api/execute", json={"code": "print('hi')", "langage": "ruby"})
        assert r.status_code == 200
        assert "non supporté" in r.json()["output"].lower() or "non supporte" in r.json()["output"].lower()

    def test_body_incomplet_422(self, client):
        r = client.post("/api/execute", json={"code": "print('hi')"})
        assert r.status_code == 422

    def test_code_vide_python(self, client):
        r = client.post("/api/execute", json={"code": "", "langage": "python"})
        assert r.status_code == 200

    def test_content_type_json(self, client):
        r = client.post("/api/execute", json={"code": "print('ok')", "langage": "python"})
        assert r.headers["content-type"].startswith("application/json")