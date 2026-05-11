"""
main.py — Point d'entrée FastAPI
Identique à l'original mais chaque responsabilité est dans son module.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from chatbot import data
from chatbot.config import HOST, PORT, STATIC_DIR

from api.chat import router as chat_router
from api.quiz import router as quiz_router
from api.exercices import router as exercices_router
from api.execute import router as execute_router
from prometheus_fastapi_instrumentator import Instrumentator 

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="EduChat API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(chat_router, prefix="/api")
app.include_router(quiz_router, prefix="/api")
app.include_router(exercices_router, prefix="/api")
app.include_router(execute_router, prefix="/api")


# ── Route langages ────────────────────────────────────────────────────────────
@app.get("/api/langages")
async def get_langages():
    return {"langages": list(data["langages"].keys())}


# ── Frontend statique ─────────────────────────────────────────────────────────
STATIC_DIR.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    html = STATIC_DIR / "index.html"
    if html.exists():
        return html.read_text(encoding="utf-8")
    return HTMLResponse("<h1>EduChat API</h1><p>Placez index.html dans /static</p>")

Instrumentator().instrument(app).expose(app)

# Lancement
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
