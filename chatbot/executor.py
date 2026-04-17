"""
chatbot/executor.py
Exécution de code utilisateur : Python, JavaScript, C.
Code 100% identique à mon_chatbot.py — juste déplacé ici.
"""

import io
import os
import contextlib
import subprocess
import tempfile

from chatbot.config import NODE_PATH, MINGW_PATH


def executer_et_capturer_sortie(code_utilisateur: str, langage: str) -> str:
    """
    Exécute le code et retourne la sortie.
    Logique identique à mon_chatbot.py.
    """
    if langage == "python":
        return _exec_python(code_utilisateur)
    elif langage == "javascript":
        return _exec_javascript(code_utilisateur)
    elif langage == "c":
        return _exec_c(code_utilisateur)
    else:
        return "Langage non supporté pour l'exécution."


# ── Python ────────────────────────────────────────────────────────────────────
def _exec_python(code: str) -> str:
    buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(buffer):
            exec(code, {})  # noqa: S102
        return buffer.getvalue().strip()
    except Exception as e:
        return f"Erreur d'exécution Python : {e}"


# ── JavaScript ────────────────────────────────────────────────────────────────
def _exec_javascript(code: str) -> str:
    with tempfile.NamedTemporaryFile(
        "w", suffix=".js", delete=False, encoding="utf-8"
    ) as tmpfile:
        tmpfile.write(code)
        tmpfile_path = tmpfile.name
    try:
        result = subprocess.run(
            [NODE_PATH, tmpfile_path], capture_output=True, text=True, timeout=30
        )
        sortie = result.stdout.strip()
        erreur = result.stderr.strip()
        if erreur:
            return f"Erreur d'exécution JS : {erreur}"
        return sortie
    except Exception as e:
        return f"Erreur lors de l'exécution JS : {e}"
    finally:
        os.remove(tmpfile_path)


# ── C ─────────────────────────────────────────────────────────────────────────
def _exec_c(code: str) -> str:
    # Ajouter MinGW au PATH (identique à mon_chatbot.py)
    os.environ["PATH"] = MINGW_PATH + ";" + os.environ["PATH"]

    with tempfile.NamedTemporaryFile(
        "w", suffix=".c", delete=False, encoding="utf-8"
    ) as tmp_c:
        tmp_c.write(code)
        c_path = tmp_c.name
    exe_path = c_path[:-2] + ".exe"

    try:
        compile_proc = subprocess.run(
            ["gcc", c_path, "-o", exe_path], capture_output=True, text=True
        )
        if compile_proc.returncode != 0:
            return f"Erreur compilation C : {compile_proc.stderr.strip()}"
        exec_proc = subprocess.run(
            [exe_path], capture_output=True, text=True, timeout=30
        )
        return exec_proc.stdout.strip()
    except Exception as e:
        return f"Erreur d'exécution C : {e}"
    finally:
        os.remove(c_path)
        if os.path.exists(exe_path):
            os.remove(exe_path)
