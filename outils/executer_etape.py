"""Exécuter uniquement le bloc demandé d'un TP."""

import argparse
import json

from admin_tools.chemins import RACINE
from admin_tools.execution import executer_etape


def main():
    catalogue = json.loads((RACINE / "catalogue.json").read_text())
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tp", choices=[t["id"] for t in catalogue])
    parser.add_argument("etape")
    parser.add_argument("--corrige", action="store_true")
    parser.add_argument("--laboratoire", action="store_true")
    args = parser.parse_args()
    tp = next(t for t in catalogue if t["id"] == args.tp)
    etape = next((e for e in tp["etapes"] if e["cle"] == args.etape), None)
    if etape is None:
        parser.error("Étapes possibles : " + ", ".join(e["cle"] for e in tp["etapes"]))
    if etape.get("laboratoire") and not args.laboratoire:
        parser.error("Cette étape nécessite --laboratoire et les machines préparées.")
    script = RACINE / tp["dossier"] / ("corrige.py" if args.corrige else "depart.py")
    executer_etape(script, args.etape, args.laboratoire)


if __name__ == "__main__":
    main()
