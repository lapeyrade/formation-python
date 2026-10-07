"""Point de contrôle Fabric du TP06, avant toute exécution Ansible."""

import argparse
import importlib.util
import json

from admin_tools.atelier import dossier_tp
from admin_tools.chemins import RACINE


def charger(nom):
    chemin = RACINE / "ateliers/06" / f"{nom}.py"
    spec = importlib.util.spec_from_file_location(nom, chemin)
    if spec is None or spec.loader is None:
        raise ImportError("Impossible de charger le module Python demandé.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--laboratoire", action="store_true", help="autoriser les accès SSH")
    parser.add_argument("--corrige", action="store_true", help="utiliser la collecte de référence")
    args = parser.parse_args()
    if not args.laboratoire:
        parser.error("Ajouter --laboratoire après préparation des accès SSH.")
    fonctions = charger("solution_collecte" if args.corrige else "mes_collectes")
    dossier = dossier_tp("tp06-collecte")
    bilan = charger("distant").executer(dossier, fonctions.collecter_parc, collecte_seule=True)
    print(json.dumps(bilan, ensure_ascii=False, indent=2))
    print(f"Point de contrôle Fabric : {dossier}")
    print("Lire collecte.csv, collecte-partielle.json et execution.log avant Ansible.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
