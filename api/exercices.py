"""api/exercices.py — Routes /api/exercices"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from chatbot import data, get_exercices_list, verifier_exercice

router = APIRouter()


class ExerciceCheckRequest(BaseModel):
    code: str
    langage: str
    exercice_index: int


@router.get("/exercices/{langage}")
async def get_exercices(langage: str):
    langage = langage.lower()
    if langage not in data["langages"]:
        raise HTTPException(404, "Langage non trouvé.")
    return {"langage": langage, "exercices": get_exercices_list(langage)}


@router.post("/exercices/check")
async def check_exercice(req: ExerciceCheckRequest):
    langage = req.langage.lower()
    if langage not in data["langages"]:
        raise HTTPException(404, "Langage non trouvé.")
    exercices = data["langages"][langage].get("exercices", [])
    if req.exercice_index >= len(exercices):
        raise HTTPException(400, "Index d'exercice invalide.")
    return verifier_exercice(langage, req.exercice_index, req.code)
