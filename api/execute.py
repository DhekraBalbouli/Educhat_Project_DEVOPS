"""api/execute.py — Route POST /api/execute"""

from fastapi import APIRouter
from pydantic import BaseModel

from chatbot import executer_et_capturer_sortie

router = APIRouter()


class CodeRequest(BaseModel):
    code: str
    langage: str


@router.post("/execute")
async def execute_code(req: CodeRequest):
    output = executer_et_capturer_sortie(req.code, req.langage.lower())
    return {"output": output, "langage": req.langage}
