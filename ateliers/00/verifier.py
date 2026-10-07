"""Contrôler les affichages d'une étape ou de tout l'atelier 0."""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("etape", nargs="?", type=int, choices=range(1, 7))
    parser.add_argument("--corrige", action="store_true", help="vérifier les corrigés fournis")
    args = parser.parse_args()
    racine = Path(__file__).resolve().parent
    attendus = json.loads((racine / "attendus.json").read_text(encoding="utf-8"))
    echecs = 0
    for numero, (nom, attendu) in enumerate(attendus.items(), 1):
        if args.etape is not None and numero != args.etape:
            continue
        script = (racine / "corriges" if args.corrige else racine) / f"{nom}.py"
        try:
            resultat = subprocess.run(
                [sys.executable, "-W", "error", str(script)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=5,
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
                check=False,
            )
        except subprocess.TimeoutExpired:
            print(f"{nom} : À revoir — exécution trop longue, vérifiez vos boucles.")
            echecs += 1
            continue
        conforme = (
            resultat.returncode == 0
            and not resultat.stderr
            and resultat.stdout.strip() == attendu.strip()
        )
        print(f"{nom} : {'Conforme' if conforme else 'À revoir'}")
        if not conforme:
            echecs += 1
            print("Attendu :\n" + attendu.rstrip())
            print("Obtenu :\n" + (resultat.stdout.strip() or "(aucun affichage)"))
            if resultat.stderr:
                print(resultat.stderr.strip())
    return 1 if echecs else 0


if __name__ == "__main__":
    raise SystemExit(main())
