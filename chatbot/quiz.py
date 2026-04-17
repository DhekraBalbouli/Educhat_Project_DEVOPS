"""
chatbot/quiz.py
Quiz et exercices.
Code 100% identique à mon_chatbot.py — juste déplacé ici.
"""

import random
from typing import Optional

from chatbot.corpus import data, langages_disponibles
from chatbot.executor import executer_et_capturer_sortie
from chatbot.text_utils import nettoyer_texte


# ── Quiz ──────────────────────────────────────────────────────────────────────
def get_quiz_questions(langage: str) -> list[dict]:
    """Retourne les questions du quiz avec options mélangées."""
    questions = data["langages"][langage].get("quizzes", [])
    result = []
    for q in questions:
        options = q["options"][:]
        random.shuffle(options)
        result.append({
            "question": q["question"],
            "options":  options,
            "answer":   q["answer"],
        })
    return result


def verifier_reponse_quiz(langage: str, question_index: int, answer: str) -> dict:
    """Vérifie une réponse de quiz. Logique identique à main.py."""
    questions = data["langages"][langage].get("quizzes", [])
    q = questions[question_index]
    correct = answer.strip().lower() == q["answer"].strip().lower()
    return {"correct": correct, "answer": q["answer"]}


# ── Exercices ─────────────────────────────────────────────────────────────────
def get_exercices_list(langage: str) -> list[dict]:
    """Retourne la liste des exercices (énoncé uniquement)."""
    exercices = data["langages"][langage].get("exercices", [])
    return [{"index": i, "enonce": e["enonce"]} for i, e in enumerate(exercices)]


def verifier_exercice(langage: str, exercice_index: int, code: str) -> dict:
    """Exécute le code et compare à la solution. Logique identique à main.py."""
    exercices = data["langages"][langage].get("exercices", [])
    exo = exercices[exercice_index]
    sortie = executer_et_capturer_sortie(code, langage)
    sortie_attendue = exo["solution"]
    correct = nettoyer_texte(sortie) == nettoyer_texte(sortie_attendue)
    return {"correct": correct, "output": sortie, "expected": sortie_attendue}


# ── Mode terminal (identique à mon_chatbot.py) ────────────────────────────────
def demander_langage() -> str:
    print("🎯 Bienvenue dans le quiz !")
    print("1. C\n2. JavaScript\n3. Python")
    try:
        choix = int(input("Votre choix (1-3) : "))
        return ["c", "javascript", "python"][choix - 1]
    except Exception:
        print("❌ Choix invalide.")
        return demander_langage()


def lancer_quiz(langage: str) -> str:
    questions_raw = data["langages"][langage].get("quizzes", [])
    if not questions_raw:
        return "❌ Aucun quiz trouvé."
    score = 0
    for i, q in enumerate(questions_raw):
        print(f"\nQuestion {i + 1}: {q['question']}")
        options = q["options"][:]
        random.shuffle(options)
        for j, opt in enumerate(options):
            print(f"{j + 1}. {opt}")
        try:
            rep = int(input("Votre réponse : "))
            if options[rep - 1].lower() == q["answer"].lower():
                print("✅ Correct !")
                score += 1
            else:
                print(f"❌ Faux. Bonne réponse : {q['answer']}")
        except Exception:
            print("❌ Entrée invalide. il faut répondre par 1, 2 ou 3")
            print(f" Bonne réponse : {q['answer']}")
    return f"\n🎯 Score final : {score}/{len(questions_raw)}"


def demarrer_quiz() -> None:
    langage = demander_langage()
    print(f"Vous avez choisi {langage.capitalize()}.\n")
    print(lancer_quiz(langage))


def afficher_exercice(langage: str) -> None:
    exercices = data["langages"][langage].get("exercices", [])
    if not exercices:
        print("❌ Aucun exercice pour ce langage.")
        return
    for i, exo in enumerate(exercices):
        print(f"\nExercice {i + 1}: {exo['enonce']}")
        print("Écris ton code ci-dessous (ligne vide pour terminer) :")
        lignes = []
        while True:
            ligne = input()
            if ligne.strip() == "":
                break
            lignes.append(ligne)
        sortie = executer_et_capturer_sortie("\n".join(lignes), langage)
        if nettoyer_texte(sortie) == nettoyer_texte(exo["solution"]):
            print("✅ Correct !")
        else:
            print(f"❌ Faux. Résultat attendu : {exo['solution']}\nTa sortie : {sortie}")


def demarrer_exercice() -> None:
    langage = input("🎯 Bienvenue dans les exercices !\nChoisir un langage (C, Python, JavaScript) : ").lower()
    if langage in ["c", "python", "javascript"]:
        afficher_exercice(langage)
    else:
        print("❌ Langage non reconnu.")