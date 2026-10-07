"""Interface guidée du TP 04 : erreurs prévues sans traceback."""

import argparse
import json
import sys
from pathlib import Path

from admin_tools.metier import analyser_logs, positif


def parseur_logs():
    parser = argparse.ArgumentParser(description="Analyseur apprenant")
    parser.add_argument("source", type=Path)
    parser.add_argument("--seuil", type=positif, default=2)
    # TODO : parser.add_argument("--sortie", type=Path, default=Path("sorties/logs")).
    # Path convertit le texte en chemin ; default garde un usage sans option explicite.
    return parser


def main():
    args = parseur_logs().parse_args()
    if not hasattr(args, "seuil") or not hasattr(args, "sortie"):
        print("À compléter : ajouter --sortie dans le parseur.")
        return 1
    try:
        bilan = analyser_logs(args.source)
        args.sortie.mkdir(parents=True, exist_ok=True)
        (args.sortie / "compteurs.json").write_text(
            json.dumps(bilan, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        alertes = {ip: n for ip, n in bilan["compteurs"].items() if n >= args.seuil}
        (args.sortie / "alertes.json").write_text(json.dumps(alertes, indent=2), encoding="utf-8")
    except (OSError, UnicodeError) as erreur:
        print(f"Lecture/écriture impossible : {erreur}", file=sys.stderr)
        return 1
    print(f"{len(bilan['compteurs'])} IP, {len(alertes)} alertes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
