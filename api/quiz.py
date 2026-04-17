"""api/quiz.py — Routes /api/quiz"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from chatbot import data, get_quiz_questions, verifier_reponse_quiz

router = APIRouter()


class QuizAnswerRequest(BaseModel):
    langage: str
    question_index: int
    answer: str


@router.get("/quiz/{langage}")
async def get_quiz(langage: str):
    langage = langage.lower()
    if langage not in data["langages"]:
        raise HTTPException(404, f"Langage '{langage}' non trouvé.")
    questions = get_quiz_questions(langage)
    if not questions:
        raise HTTPException(404, "Aucun quiz disponible pour ce langage.")
    return {"langage": langage, "questions": questions}


@router.post("/quiz/check")
async def check_quiz_answer(req: QuizAnswerRequest):
    langage = req.langage.lower()
    if langage not in data["langages"]:
        raise HTTPException(404, "Langage non trouvé.")
    questions = data["langages"][langage].get("quizzes", [])
    if req.question_index >= len(questions):
        raise HTTPException(400, "Index de question invalide.")
    return verifier_reponse_quiz(langage, req.question_index, req.answer)
