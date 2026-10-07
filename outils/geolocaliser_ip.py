"""Interroger explicitement un service public pour une IP publique connue."""

import argparse
import json
from pathlib import Path

from admin_tools.services import geolocaliser_publique


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ip", help="adresse publique ; exemple : 1.1.1.1")
    parser.add_argument(
        "--sortie", type=Path, default=Path("sorties/geolocalisation-publique.json")
    )
    args = parser.parse_args()
    try:
        resultat = geolocaliser_publique(args.ip)
    except ValueError as erreur:
        parser.error(str(erreur))
    args.sortie.parent.mkdir(parents=True, exist_ok=True)
    args.sortie.write_text(json.dumps(resultat, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(resultat, ensure_ascii=False))
    return 0 if resultat["statut"] == "localisee" else 1


if __name__ == "__main__":
    raise SystemExit(main())
