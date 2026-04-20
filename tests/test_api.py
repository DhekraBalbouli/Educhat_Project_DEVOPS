"""
On utilise TestClient qui simule de vraies requêtes HTTP
sans avoir besoin de démarrer le serveur.

Pour chaque route on vérifie :
  - Le code HTTP (200, 404, 422...)
  - Que la réponse contient les bonnes clés
  - Que les valeurs sont du bon type
"""

from fastapi.testclient import TestClient
from main import app

# Un seul client pour tous les tests de ce fichier
client = TestClient(app)


# ════════════════════════════════════════════
# GET /api/langages
# ════════════════════════════════════════════


def test_langages_retourne_200():
    """L'API doit répondre avec un code 200."""
    r = client.get("/api/langages")
    assert r.status_code == 200


def test_langages_contient_liste():
    """La réponse doit contenir une clé 'langages' avec une liste."""
    r = client.get("/api/langages")
    assert "langages" in r.json()
    assert isinstance(r.json()["langages"], list)


def test_langages_contient_python():
    r = client.get("/api/langages")
    assert "python" in r.json()["langages"]


def test_langages_contient_javascript():
    r = client.get("/api/langages")
    assert "javascript" in r.json()["langages"]


def test_langages_contient_c():
    r = client.get("/api/langages")
    assert "c" in r.json()["langages"]


# ════════════════════════════════════════════
# POST /api/chat
# ════════════════════════════════════════════


def test_chat_retourne_200():
    r = client.post("/api/chat", json={"message": "bonjour"})
    assert r.status_code == 200


def test_chat_bonjour_est_salutation():
    """'bonjour' doit être reconnu comme une salutation."""
    r = client.post("/api/chat", json={"message": "bonjour"})
    assert r.json()["type"] == "salutation"


def test_chat_reponse_non_vide():
    """Le chatbot doit toujours retourner une réponse."""
    r = client.post("/api/chat", json={"message": "bonjour"})
    assert len(r.json()["response"]) > 0


def test_chat_question_python_retourne_200():
    r = client.post("/api/chat", json={"message": "c est quoi python"})
    assert r.status_code == 200


def test_chat_structure_reponse():
    """La réponse doit avoir les clés : response, langage, type."""
    r = client.post("/api/chat", json={"message": "python"})
    body = r.json()
    assert "response" in body
    assert "langage" in body
    assert "type" in body


def test_chat_message_manquant_retourne_422():
    """Sans message, l'API doit retourner une erreur de validation."""
    r = client.post("/api/chat", json={})
    assert r.status_code == 422


# ════════════════════════════════════════════
# GET /api/quiz/{langage}
# ════════════════════════════════════════════


def test_quiz_python_retourne_200():
    r = client.get("/api/quiz/python")
    assert r.status_code == 200


def test_quiz_javascript_retourne_200():
    r = client.get("/api/quiz/javascript")
    assert r.status_code == 200


def test_quiz_c_retourne_200():
    r = client.get("/api/quiz/c")
    assert r.status_code == 200


def test_quiz_contient_questions():
    """La réponse doit contenir une liste de questions."""
    r = client.get("/api/quiz/python")
    assert "questions" in r.json()
    assert len(r.json()["questions"]) > 0


def test_quiz_structure_question():
    """Chaque question doit avoir : question, options, answer."""
    r = client.get("/api/quiz/python")
    q = r.json()["questions"][0]
    assert "question" in q
    assert "options" in q
    assert "answer" in q


def test_quiz_bonne_reponse_dans_options():
    """La bonne réponse doit être dans les options."""
    r = client.get("/api/quiz/python")
    for q in r.json()["questions"]:
        assert q["answer"] in q["options"]


def test_quiz_langage_inexistant_retourne_404():
    """Un langage qui n'existe pas doit retourner 404."""
    r = client.get("/api/quiz/cobol")
    assert r.status_code == 404


# ════════════════════════════════════════════
# POST /api/quiz/check
# ════════════════════════════════════════════


def test_quiz_check_bonne_reponse():
    """Envoyer la bonne réponse doit retourner correct=True."""
    # On récupère d'abord la bonne réponse
    questions = client.get("/api/quiz/python").json()["questions"]
    bonne_reponse = questions[0]["answer"]

    r = client.post(
        "/api/quiz/check",
        json={"langage": "python", "question_index": 0, "answer": bonne_reponse},
    )
    assert r.status_code == 200
    assert r.json()["correct"] is True


def test_quiz_check_mauvaise_reponse():
    """Envoyer une mauvaise réponse doit retourner correct=False."""
    r = client.post(
        "/api/quiz/check",
        json={
            "langage": "python",
            "question_index": 0,
            "answer": "reponse_completement_fausse",
        },
    )
    assert r.json()["correct"] is False


def test_quiz_check_langage_inexistant():
    r = client.post(
        "/api/quiz/check",
        json={"langage": "cobol", "question_index": 0, "answer": "test"},
    )
    assert r.status_code == 404


# ════════════════════════════════════════════
# GET /api/exercices/{langage}
# ════════════════════════════════════════════


def test_exercices_python_retourne_200():
    r = client.get("/api/exercices/python")
    assert r.status_code == 200


def test_exercices_contient_liste():
    r = client.get("/api/exercices/python")
    assert "exercices" in r.json()
    assert len(r.json()["exercices"]) > 0


def test_exercices_structure():
    """Chaque exercice doit avoir un index et un énoncé."""
    r = client.get("/api/exercices/python")
    exo = r.json()["exercices"][0]
    assert "index" in exo
    assert "enonce" in exo


def test_exercices_solution_non_exposee():
    """La solution NE DOIT PAS être visible par l'utilisateur."""
    r = client.get("/api/exercices/python")
    for exo in r.json()["exercices"]:
        assert "solution" not in exo


def test_exercices_langage_inexistant_retourne_404():
    r = client.get("/api/exercices/cobol")
    assert r.status_code == 404


# ════════════════════════════════════════════
# POST /api/exercices/check
# ════════════════════════════════════════════


def test_exercice_check_retourne_200():
    r = client.post(
        "/api/exercices/check",
        json={"code": "print('test')", "langage": "python", "exercice_index": 0},
    )
    assert r.status_code == 200


def test_exercice_check_structure_reponse():
    """La réponse doit avoir : correct, output, expected."""
    r = client.post(
        "/api/exercices/check",
        json={"code": "print('test')", "langage": "python", "exercice_index": 0},
    )
    body = r.json()
    assert "correct" in body
    assert "output" in body
    assert "expected" in body


def test_exercice_check_index_invalide_retourne_400():
    r = client.post(
        "/api/exercices/check",
        json={"code": "print('test')", "langage": "python", "exercice_index": 9999},
    )
    assert r.status_code == 400


# ════════════════════════════════════════════
# POST /api/execute  (bac à sable)
# ════════════════════════════════════════════


def test_execute_python_retourne_200():
    r = client.post("/api/execute", json={"code": "print('ok')", "langage": "python"})
    assert r.status_code == 200


def test_execute_python_sortie_correcte():
    r = client.post(
        "/api/execute", json={"code": "print('Hello')", "langage": "python"}
    )
    assert r.json()["output"] == "Hello"


def test_execute_python_calcul():
    r = client.post("/api/execute", json={"code": "print(10 + 5)", "langage": "python"})
    assert r.json()["output"] == "15"


def test_execute_erreur_pas_500():
    """Une erreur dans le code ne doit pas faire planter le serveur (pas de 500)."""
    r = client.post("/api/execute", json={"code": "print(1/0)", "langage": "python"})
    assert r.status_code == 200


def test_execute_langage_inconnu():
    """Un langage non supporté doit retourner un message, pas une erreur serveur."""
    r = client.post("/api/execute", json={"code": "print('hi')", "langage": "ruby"})
    assert r.status_code == 200
    assert "non support" in r.json()["output"].lower()


def test_execute_champs_manquants_retourne_422():
    r = client.post("/api/execute", json={"code": "print('hi')"})
    assert r.status_code == 422
