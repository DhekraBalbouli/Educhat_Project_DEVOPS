"""
mon_chatbot.py — Mode terminal (inchangé)
Maintenant il importe depuis le package chatbot/
au lieu de tout contenir lui-même.
"""

from chatbot import (
    salutations,
    detecter_langage,
    repondre_question,
    langages_disponibles,
    demarrer_quiz,
    demarrer_exercice,
)

RESET = "\033[0m"
EDUCHAT_COLOR = "\033[92;1m"
USER_COLOR = "\033[96m"
EXIT_COLOR = "\033[91;1m"

if __name__ == "__main__":
    print(
        f"{EDUCHAT_COLOR}💬 EduChat : Bienvenue ! Pose une question, demande un quiz ou un exercice. (Tape 'exit' pour quitter){RESET}"
    )

    while True:
        question = input(f"{USER_COLOR}👤 Toi : {RESET}").strip().lower()

        if question in ["exit", "quit", "bye"]:
            print(f"{EXIT_COLOR}👋 EduChat : À bientôt !{RESET}")
            break

        for mot, rep in salutations.items():
            if mot in question:
                print(f"{EDUCHAT_COLOR}🤖 EduChat : {rep}{RESET}")
                break
        else:
            if "quiz" in question:
                demarrer_quiz()
            elif "exercice" in question:
                demarrer_exercice()
            else:
                langage = detecter_langage(question, langages_disponibles)
                reponse = repondre_question(question)
                print(f"{EDUCHAT_COLOR}🤖 EduChat ({langage}) : {reponse}{RESET}")
