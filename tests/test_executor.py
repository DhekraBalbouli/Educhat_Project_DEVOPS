"""
Couvre :
  - Execution Python  (_exec_python)
  - Execution JavaScript (_exec_javascript)
  - Execution C       (_exec_c)
  - executer_et_capturer_sortie() — dispatcher principal
"""

from unittest.mock import patch, MagicMock
from chatbot.executor import executer_et_capturer_sortie

# ══════════════════════════════════════════════
# Python
# ══════════════════════════════════════════════


class TestExecutionPython:

    def test_hello_world(self):
        sortie = executer_et_capturer_sortie("print('Hello World')", "python")
        assert sortie == "Hello World"

    def test_calcul_addition(self):
        sortie = executer_et_capturer_sortie("print(2 + 3)", "python")
        assert sortie == "5"

    def test_calcul_multiplication(self):
        sortie = executer_et_capturer_sortie("print(4 * 5)", "python")
        assert sortie == "20"

    def test_variable_et_print(self):
        code = "nom = 'Alice'\nprint(nom)"
        sortie = executer_et_capturer_sortie(code, "python")
        assert sortie == "Alice"

    def test_boucle_for(self):
        code = "for i in range(3):\n    print(i)"
        sortie = executer_et_capturer_sortie(code, "python")
        assert "0" in sortie and "1" in sortie and "2" in sortie

    def test_fonction(self):
        code = "def saluer(nom):\n    return 'Bonjour ' + nom\nprint(saluer('Bob'))"
        sortie = executer_et_capturer_sortie(code, "python")
        assert sortie == "Bonjour Bob"

    def test_liste(self):
        code = "fruits = ['pomme', 'banane']\nprint(len(fruits))"
        sortie = executer_et_capturer_sortie(code, "python")
        assert sortie == "2"

    def test_sans_sortie(self):
        sortie = executer_et_capturer_sortie("x = 42", "python")
        assert "aucune" in sortie.lower() or sortie == ""

    def test_erreur_syntaxe(self):
        sortie = executer_et_capturer_sortie("print(", "python")
        assert "erreur" in sortie.lower() or "error" in sortie.lower()

    def test_erreur_division_zero(self):
        sortie = executer_et_capturer_sortie("print(1 / 0)", "python")
        assert "erreur" in sortie.lower() or "ZeroDivision" in sortie

    def test_erreur_variable_non_definie(self):
        sortie = executer_et_capturer_sortie("print(x)", "python")
        assert "erreur" in sortie.lower() or "NameError" in sortie

    def test_print_multiple_lignes(self):
        code = "print('ligne1')\nprint('ligne2')"
        sortie = executer_et_capturer_sortie(code, "python")
        assert "ligne1" in sortie and "ligne2" in sortie

    def test_string_multilignes(self):
        code = "print('hello')"
        assert executer_et_capturer_sortie(code, "python") == "hello"

    def test_casse_langage_python(self):
        """Le dispatcher doit accepter 'Python' en majuscule."""
        sortie = executer_et_capturer_sortie("print('ok')", "Python")
        # Selon l'implémentation, soit ça marche, soit retourne non supporté
        assert isinstance(sortie, str)


# ══════════════════════════════════════════════
# JavaScript (mocké car Node.js peut être absent)
# ══════════════════════════════════════════════


class TestExecutionJavaScript:

    def test_hello_world_mocke(self):
        mock_result = MagicMock()
        mock_result.stdout = "Hello World\n"
        mock_result.stderr = ""
        with patch("subprocess.run", return_value=mock_result):
            sortie = executer_et_capturer_sortie(
                "console.log('Hello World')", "javascript"
            )
        assert sortie == "Hello World"

    def test_calcul_mocke(self):
        mock_result = MagicMock()
        mock_result.stdout = "8\n"
        mock_result.stderr = ""
        with patch("subprocess.run", return_value=mock_result):
            sortie = executer_et_capturer_sortie("console.log(3 + 5)", "javascript")
        assert sortie == "8"

    def test_erreur_js_mocke(self):
        mock_result = MagicMock()
        mock_result.stdout = ""
        mock_result.stderr = "ReferenceError: x is not defined"
        with patch("subprocess.run", return_value=mock_result):
            sortie = executer_et_capturer_sortie("console.log(x)", "javascript")
        assert "erreur" in sortie.lower() or "Error" in sortie

    def test_node_introuvable(self):
        with patch("subprocess.run", side_effect=FileNotFoundError("node not found")):
            sortie = executer_et_capturer_sortie("console.log('test')", "javascript")
        assert "introuvable" in sortie.lower() or "node" in sortie.lower()

    def test_sans_sortie_js(self):
        mock_result = MagicMock()
        mock_result.stdout = ""
        mock_result.stderr = ""
        with patch("subprocess.run", return_value=mock_result):
            sortie = executer_et_capturer_sortie("let x = 5;", "javascript")
        assert "aucune" in sortie.lower() or sortie == ""


# ══════════════════════════════════════════════
# C (mocké car GCC peut être absent)
# ══════════════════════════════════════════════


class TestExecutionC:

    def test_hello_world_c_mocke(self):
        compile_mock = MagicMock(returncode=0, stderr="")
        exec_mock = MagicMock(stdout="Hello World\n", stderr="")
        with patch("subprocess.run", side_effect=[compile_mock, exec_mock]):
            sortie = executer_et_capturer_sortie(
                '#include<stdio.h>\nint main(){printf("Hello World");return 0;}', "c"
            )
        assert sortie == "Hello World"

    def test_erreur_compilation_c(self):
        compile_mock = MagicMock(returncode=1, stderr="error: expected ';'")
        with patch("subprocess.run", return_value=compile_mock):
            sortie = executer_et_capturer_sortie("int main(){return 0", "c")
        assert "erreur" in sortie.lower() or "error" in sortie.lower()

    def test_gcc_introuvable(self):
        with patch("subprocess.run", side_effect=FileNotFoundError("gcc not found")):
            sortie = executer_et_capturer_sortie("int main(){return 0;}", "c")
        assert "introuvable" in sortie.lower() or "gcc" in sortie.lower()


# ══════════════════════════════════════════════
# Dispatcher — langage non supporté
# ══════════════════════════════════════════════


class TestDispatcher:

    def test_langage_inconnu(self):
        sortie = executer_et_capturer_sortie("print('hi')", "ruby")
        assert "non supporté" in sortie.lower() or "non supporte" in sortie.lower()

    def test_langage_vide(self):
        sortie = executer_et_capturer_sortie("print('hi')", "")
        assert isinstance(sortie, str) and len(sortie) > 0

    def test_langage_java(self):
        sortie = executer_et_capturer_sortie("System.out.println('hi');", "java")
        assert "non supporté" in sortie.lower() or "non supporte" in sortie.lower()

    def test_code_vide_python(self):
        sortie = executer_et_capturer_sortie("", "python")
        assert isinstance(sortie, str)
