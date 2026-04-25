"""
chatbot/config.py
Toute la configuration du projet en un seul endroit.
Extrait de mon_chatbot.py — rien n'est modifié, juste centralisé.
"""
 
import os
import shutil
from pathlib import Path
 
#  Chemins ───────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).resolve().parent.parent
NODE_PATH  = shutil.which("node") or ""   # → /usr/bin/node sur Linux
MINGW_PATH = shutil.which("gcc")  or ""   # → /usr/bin/gcc  sur Linux

# ─ Compilateurs (identiques à mon_chatbot.py) ────────────────────────────────
NODE_PATH  = r"C:\Program Files\nodejs\node.exe"
MINGW_PATH = r"C:\MinGW\bin"
 
# ── Serveur 
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))
 
# ── Seuils de matching (identiques à mon_chatbot.py) ─────────────────────────
DIFFLIB_CUTOFF      = 0.5   # cutoff get_close_matches
RATIO_MIN           = 0.6   # ratio SequenceMatcher minimum
FUZZ_THRESHOLD      = 75    # seuil rapidfuzz partial_ratio
CONFIDENCE_HIGH     = 0.8   # confiance ChatterBot haute
CONFIDENCE_MID      = 0.5   # confiance ChatterBot moyenne
