import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


# ── Fixture : client FastAPI ──────────────────────────────────────────────────
@pytest.fixture(scope="session")
def client():
    """
    Client HTTP de test FastAPI.
    scope="session" : créé une seule fois pour tous les tests → rapide.
    """
    from main import app

    return TestClient(app)


# ── Fixture : données YAML mockées ────────────────────────────────────────────
@pytest.fixture
def sample_data():
    """
    Données YAML minimales pour les tests qui n'ont pas besoin
    du vrai fichier langages.yml.
    """
    return {
        "langages": {
            "python": {
                "conversations": [
                    {
                        "question": "c'est quoi python",
                        "answers": [
                            "Python est un langage de programmation interprete."
                        ],
                    },
                    {
                        "question": "comment faire une boucle en python",
                        "answers": ["Utilise for i in range(n): ou while condition:"],
                    },
                ],
                "quizzes": [
                    {
                        "question": "Quel mot-cle definit une fonction en Python ?",
                        "options": ["def", "function", "fun", "define"],
                        "answer": "def",
                    },
                    {
                        "question": "Quelle est la sortie de print(2 + 3) ?",
                        "options": ["5", "23", "2+3", "Erreur"],
                        "answer": "5",
                    },
                ],
                "exercices": [
                    {
                        "enonce": "Affiche 'Hello World' avec print()",
                        "solution": "Hello World",
                    }
                ],
            },
            "javascript": {
                "conversations": [
                    {
                        "question": "c'est quoi javascript",
                        "answers": ["JavaScript est le langage du web."],
                    }
                ],
                "quizzes": [
                    {
                        "question": "Quel mot-cle declare une variable en JS ?",
                        "options": ["let", "var", "const", "int"],
                        "answer": "let",
                    }
                ],
                "exercices": [
                    {
                        "enonce": "Affiche 'Hello' avec console.log()",
                        "solution": "Hello",
                    }
                ],
            },
            "c": {
                "conversations": [
                    {
                        "question": "c'est quoi le langage c",
                        "answers": ["C est un langage compile cree en 1972."],
                    }
                ],
                "quizzes": [
                    {
                        "question": "Quelle fonction affiche du texte en C ?",
                        "options": ["printf", "print", "cout", "echo"],
                        "answer": "printf",
                    }
                ],
                "exercices": [
                    {"enonce": "Affiche Hello avec printf", "solution": "Hello"}
                ],
            },
        }
    }


# ── Fixture : mock Mistral API ────────────────────────────────────────────────
@pytest.fixture
def mock_mistral_success():
    """Simule une réponse Mistral réussie."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Voici une explication de Python."}}]
    }
    with patch("requests.post", return_value=mock_response) as mock:
        yield mock


@pytest.fixture
def mock_mistral_failure():
    """Simule une panne de l'API Mistral."""
    with patch("requests.post", side_effect=Exception("Connection refused")) as mock:
        yield mock


@pytest.fixture
def mock_mistral_timeout():
    """Simule un timeout Mistral."""
    import requests

    with patch("requests.post", side_effect=requests.exceptions.Timeout()) as mock:
        yield mock
