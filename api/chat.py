"""api/chat.py — Route POST /api/chat"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from chatbot import salutations, detecter_langage, repondre_question, langages_disponibles

router = APIRouter()


class MessageRequest(BaseModel):
    message: str


@router.post("/chat")
async def chat(req: MessageRequest):
    msg = req.message.strip().lower()

    # Salutations — logique identique à main.py original
    for mot, rep in salutations.items():
        if mot in msg:
            return {"response": rep, "langage": None, "type": "salutation"}

    langage = detecter_langage(msg, langages_disponibles)
    reponse = repondre_question(req.message)
    return {"response": reponse, "langage": langage, "type": "question"}