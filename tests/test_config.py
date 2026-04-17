"""
tests/test_config.py
Tests unitaires — chatbot/config.py

Vérifie que la configuration est correctement définie
et que les chemins existent.
"""

from pathlib import Path


class TestConfig:

    def test_base_dir_existe(self):
        from chatbot.config import BASE_DIR

        assert BASE_DIR.exists(), f"BASE_DIR n'existe pas : {BASE_DIR}"

    def test_yaml_path_existe(self):
        from chatbot.config import YAML_PATH

        assert YAML_PATH.exists(), f"Fichier YAML introuvable : {YAML_PATH}"

    def test_yaml_path_est_fichier(self):
        from chatbot.config import YAML_PATH

        assert YAML_PATH.is_file()

    def test_static_dir_est_path(self):
        from chatbot.config import STATIC_DIR

        assert isinstance(STATIC_DIR, Path)

    def test_host_est_chaine(self):
        from chatbot.config import HOST

        assert isinstance(HOST, str)
        assert len(HOST) > 0

    def test_port_est_entier(self):
        from chatbot.config import PORT

        assert isinstance(PORT, int)
        assert 1024 <= PORT <= 65535, f"Port hors plage : {PORT}"

    def test_port_par_defaut(self):
        from chatbot.config import PORT

        assert PORT == 8000

    def test_difflib_cutoff_valide(self):
        from chatbot.config import DIFFLIB_CUTOFF

        assert 0.0 < DIFFLIB_CUTOFF < 1.0

    def test_ratio_min_valide(self):
        from chatbot.config import RATIO_MIN

        assert 0.0 < RATIO_MIN < 1.0

    def test_fuzz_threshold_valide(self):
        from chatbot.config import FUZZ_THRESHOLD

        assert 0 < FUZZ_THRESHOLD <= 100

    def test_confidence_high_superieur_mid(self):
        from chatbot.config import CONFIDENCE_HIGH, CONFIDENCE_MID

        assert CONFIDENCE_HIGH > CONFIDENCE_MID

    def test_node_path_est_chaine(self):
        from chatbot.config import NODE_PATH

        assert isinstance(NODE_PATH, str)

    def test_mingw_path_est_chaine(self):
        from chatbot.config import MINGW_PATH

        assert isinstance(MINGW_PATH, str)

    def test_variables_env_host(self, monkeypatch):
        """HOST doit être surchargeable par variable d'environnement."""
        monkeypatch.setenv("HOST", "0.0.0.0")
        import importlib
        import chatbot.config as cfg

        importlib.reload(cfg)
        assert cfg.HOST == "0.0.0.0"
        # Remettre la valeur par défaut
        monkeypatch.delenv("HOST", raising=False)
        importlib.reload(cfg)

    def test_variables_env_port(self, monkeypatch):
        """PORT doit être surchargeable par variable d'environnement."""
        monkeypatch.setenv("PORT", "9000")
        import importlib
        import chatbot.config as cfg

        importlib.reload(cfg)
        assert cfg.PORT == 9000
        monkeypatch.delenv("PORT", raising=False)
        importlib.reload(cfg)
