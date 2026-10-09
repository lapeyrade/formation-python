"""Préparer l'inventaire de l'atelier 7 en réutilisant les accès du TP6."""

import argparse
from pathlib import Path

from ansible_support import KIT, preparer


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local", action="store_true", help="mode local explicite, sans SSH")
    parser.add_argument("--corrige", action="store_true", help="déployer la correction Python")
    parser.add_argument("--sortie", type=Path, default=KIT)
    args = parser.parse_args()
    try:
        destination = preparer(args.sortie, args.local, args.corrige)
    except (OSError, ValueError, KeyError, TypeError) as erreur:
        print("À résoudre :", erreur)
        return 2
    print("Inventaire prêt :", destination)
    print("Cible : vm-locale ; dossier de déploiement : ~/pyx-tp07-ansible")
    print("Mode :", "local sans SSH" if args.local else "SSH réutilisé du TP6")
    print("Aucun fichier du TP6, accès SSH ou service n'a été modifié.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
