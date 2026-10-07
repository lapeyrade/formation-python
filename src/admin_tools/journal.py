"""Journal technique séparé des données métier, sans modifier le logger global."""

import logging
import time
from contextlib import contextmanager


@contextmanager
def journal_execution(dossier):
    """Une exécution, un fichier UTF-8 ; fermeture garantie même après une erreur."""
    logger = logging.Logger("pyx.execution", level=logging.INFO)
    logger.propagate = False
    handler = logging.FileHandler(dossier / "execution.log", mode="w", encoding="utf-8")
    formatter = logging.Formatter(
        "%(asctime)sZ %(levelname)s etape=%(etape)s cible=%(cible)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
        defaults={"etape": "global", "cible": "local"},
    )
    formatter.converter = time.gmtime
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    try:
        yield logger
    except Exception as erreur:
        # Tracer puis propager : un log ne transforme pas une erreur en succès.
        logger.error("traitement interrompu (%s)", type(erreur).__name__)
        raise
    finally:
        logger.removeHandler(handler)
        handler.close()
