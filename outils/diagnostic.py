"""Vérifier le projet dans le poste de travail Linux, puis les accès SSH séparément."""

import argparse
import importlib
import importlib.metadata
import json
import platform
import shutil
import subprocess
import sys
import tempfile

from admin_tools.chemins import DONNEES, RACINE
from admin_tools.distant import charger_inventaire, collecter
from admin_tools.metier import analyser_logs, lire_inventaire


def main():
    parseur = argparse.ArgumentParser(description=__doc__)
    parseur.add_argument(
        "--distant", action="store_true", help="contrôler les accès SSH configurés"
    )
    options = parseur.parse_args()
    try:
        if sys.version_info[:2] != (3, 13):
            raise ValueError("Utiliser le Python 3.13 du projet avec uv run.")
        for nom in ["pandas", "openpyxl", "requests", "scrapy", "fabric", "aiosmtpd", "ma_boite"]:
            importlib.import_module(nom)
        import pandas as pd

        machines, rejets = lire_inventaire(DONNEES / "parc_source.csv")
        assert len(machines) == 8 and len(rejets) == 2
        assert len(pd.read_excel(DONNEES / "inventaire.xlsx")) == 8
        assert sum(analyser_logs(DONNEES / "auth.log")["compteurs"].values()) == 6
        sorties = RACINE / "sorties"
        sorties.mkdir(exist_ok=True)
        with tempfile.TemporaryFile(dir=sorties) as fichier:
            fichier.write(b"diagnostic")
        print(f"Python {sys.version.split()[0]} — imports, bibliothèque locale et données : OK")
        print(f"Poste : {platform.node()} ; système : {platform.system()} ; écriture : OK")
        print(f"Interpréteur du projet : {sys.executable}")
        for nom in ["pandas", "scrapy", "fabric"]:
            print(f"{nom} {importlib.metadata.version(nom)}")
        if platform.system() != "Windows":
            importlib.import_module("ansible")
            executable = shutil.which("ansible-playbook")
            if executable is None:
                raise ValueError("Ansible absent : relancer uv sync --locked.")
            resultat = subprocess.run(
                [executable, "--version"], capture_output=True, text=True, timeout=10
            )
            if resultat.returncode or "[WARNING]" in resultat.stdout + resultat.stderr:
                raise ValueError("La vérification Ansible a échoué : examiner sa configuration.")
            print(f"Ansible natif {importlib.metadata.version('ansible-core')} : OK")
        if options.distant:
            if not shutil.which("ssh"):
                raise ValueError("Client ssh absent du poste.")
            inventaire = charger_inventaire()
            mesures = collecter(inventaire=inventaire)
            if any(m["statut"] != "ok" or m["systeme"] != "Linux" for m in mesures):
                print(json.dumps(mesures, ensure_ascii=False, indent=2))
                raise ValueError(
                    "Toutes les cibles Linux configurées doivent être joignables avant le TP 06."
                )
            print(f"{len(mesures)} cible(s) SSH configurée(s) : OK")
        else:
            print("SSH non contrôlé : lancer ce diagnostic avec --distant après configuration.")
    except (OSError, ValueError, ImportError, AssertionError, subprocess.TimeoutExpired) as erreur:
        print(f"À résoudre : {erreur}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
