"""Créer une dérive contrôlée : seuil 10 et permissions 0600, avec sauvegarde."""

import argparse
from pathlib import Path

from ansible_support import KIT, creer_derive, deploiement, mettre_support_de_cote


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventaire", type=Path, default=KIT)
    parser.add_argument(
        "--fichier-absent", action="store_true", help="Déplacer support.py en sauvegarde."
    )
    args = parser.parse_args()
    try:
        dossier = deploiement(args.inventaire)
        copie = mettre_support_de_cote(dossier) if args.fichier_absent else creer_derive(dossier)
    except (OSError, ValueError, KeyError, TypeError) as erreur:
        print("À résoudre :", erreur)
        return 2
    if args.fichier_absent:
        print("Incident créé : support.py déplacé en sauvegarde, sans suppression.")
    else:
        print("Dérive créée : seuil 10 %, permissions 0600.")
    print("Fichier initial conservé :", copie)
    print("Relire, prévisualiser la réparation, puis réappliquer le playbook.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
