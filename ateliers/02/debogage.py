"""Deux erreurs volontairement capturées pour apprendre à lire un traceback.

Corriger prioritaire et lire_note, puis relancer le même cas.
--corrige montre la référence ; ce fichier ne participe pas au bilan du TP.
"""

import argparse
import sys
import tempfile
import traceback
from pathlib import Path


def prioritaire(machine, seuil=80):
    # À écrire : convertir la charge issue du CSV avant de la comparer.
    return machine["charge"] >= seuil


def lire_note(dossier):
    # À écrire : utiliser le nom du fichier créé par la démonstration.
    return (dossier / "note.txt").read_text(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cas", choices=["type", "chemin"], default="type")
    parser.add_argument("--corrige", action="store_true")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="pyx-debogage-") as temporaire:
        dossier = Path(temporaire)
        (dossier / "intervention.txt").write_text("Contrôle du parc\n", encoding="utf-8")
        try:
            if args.cas == "type":
                machine = {"nom": "srv-paris-web-01", "charge": "85"}
                resultat = int(machine["charge"]) >= 80 if args.corrige else prioritaire(machine)
            else:
                resultat = (
                    (dossier / "intervention.txt").read_text(encoding="utf-8")
                    if args.corrige
                    else lire_note(dossier)
                )
        except (TypeError, FileNotFoundError):
            print("Erreur volontaire capturée pour lecture :")
            traceback.print_exc(file=sys.stdout)
            print("Repérer le type, la dernière ligne du code et la valeur en cause.")
        else:
            print("Cas résolu :", str(resultat).strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
