"""Vérifier l'un des six TP : production principale ou ensemble des étapes."""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from admin_tools.chemins import RACINE
from admin_tools.validation import verifier_productions


def verifier(tp, corrige=False, complet=False, laboratoire=False, etape_seule=None):
    identifiant = tp["id"]
    script = RACINE / tp["dossier"] / ("corrige.py" if corrige else "depart.py")
    parent = RACINE / "sorties" / "verifications"
    parent.mkdir(parents=True, exist_ok=True)
    dossier = Path(tempfile.mkdtemp(prefix=f"{identifiant}-", dir=parent))
    env = os.environ.copy()
    env["PYX_DOSSIER"] = str(dossier)
    env["PYTHONWARNINGS"] = "error"
    debut = time.perf_counter()
    commande = [sys.executable, "-W", "error", str(script)]
    if etape_seule:
        commande = [
            sys.executable,
            "-W",
            "error",
            str(RACINE / "outils/executer_etape.py"),
            identifiant,
            etape_seule,
        ]
        if corrige:
            commande.append("--corrige")
    if laboratoire and identifiant == "tp06":
        commande.append("--laboratoire")
    try:
        r = subprocess.run(
            commande, cwd=RACINE, env=env, capture_output=True, text=True, timeout=90
        )
    except subprocess.TimeoutExpired:
        return {"id": identifiant, "ok": False, "message": "Délai de 90 s dépassé."}
    if r.returncode or r.stderr:
        return {
            "id": identifiant,
            "ok": False,
            "message": r.stderr.strip() or r.stdout.strip(),
            "code": r.returncode,
        }
    try:
        bilan = json.loads((dossier / "bilan.json").read_text())
    except (OSError, ValueError):
        return {"id": identifiant, "ok": False, "message": "Bilan absent ou invalide."}
    if not isinstance(bilan, dict) or not isinstance(bilan.get("resultat"), dict):
        return {"id": identifiant, "ok": False, "message": "Bilan à compléter."}
    controles, non_verifiees = {}, []
    for etape in tp["etapes"]:
        cle = etape["cle"]
        if etape_seule and cle != etape_seule:
            non_verifiees.append(cle)
            continue
        demande_explicitement = bool(etape.get("laboratoire") and laboratoire)
        if (
            not etape_seule and not complet and cle != tp["principal"] and not demande_explicitement
        ) or (etape.get("laboratoire") and not laboratoire):
            non_verifiees.append(cle)
            continue
        obtenu = bilan["resultat"].get(cle)
        if not isinstance(obtenu, dict) or all(v is None for v in obtenu.values()):
            controles[cle] = "À compléter"
            continue
        try:
            verifier_productions(cle, dossier / cle)
        except Exception as erreur:
            controles[cle] = f"Production à corriger : {erreur}"
            continue
        differences = {
            key: {"attendu": value, "obtenu": obtenu.get(key)}
            for key, value in etape["attendus"].items()
            if obtenu.get(key) != value
        }
        controles[cle] = differences or "Conforme"
    ok = bool(controles) and all(c == "Conforme" for c in controles.values())
    return {
        "id": identifiant,
        "ok": ok,
        "portee": (
            f"étape {etape_seule}"
            if etape_seule
            else "toutes les étapes disponibles"
            if complet
            else "production principale et laboratoire"
            if laboratoire and identifiant == "tp06"
            else "production principale"
        ),
        "message": controles,
        "non_verifiees": non_verifiees,
        "secondes": round(time.perf_counter() - debut, 3),
        "dossier": str(dossier),
    }


def main():
    catalogue = json.loads((RACINE / "catalogue.json").read_text())
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tp", choices=[t["id"] for t in catalogue] + ["tous"])
    parser.add_argument("--corrige", action="store_true")
    parser.add_argument("--complet", action="store_true", help="contrôler aussi les étapes guidées")
    parser.add_argument(
        "--laboratoire", action="store_true", help="inclure Fabric/Ansible au TP 06"
    )
    parser.add_argument("--etape", help="exécuter et vérifier uniquement cette étape")
    parser.add_argument("--rapport", type=Path)
    args = parser.parse_args()
    if args.etape:
        if args.tp == "tous" or args.complet:
            parser.error("--etape demande un seul TP et ne se combine pas avec --complet.")
        tp = next(t for t in catalogue if t["id"] == args.tp)
        etape = next((e for e in tp["etapes"] if e["cle"] == args.etape), None)
        if etape is None:
            parser.error("Étapes possibles : " + ", ".join(e["cle"] for e in tp["etapes"]))
        if etape.get("laboratoire") and not args.laboratoire:
            parser.error("Cette étape nécessite --laboratoire et les machines préparées.")
        if args.laboratoire and not etape.get("laboratoire"):
            parser.error("Avec --etape, --laboratoire s’utilise uniquement pour distant.")
    resultats = [
        verifier(t, args.corrige, args.complet, args.laboratoire, args.etape)
        for t in catalogue
        if args.tp == "tous" or args.tp == t["id"]
    ]
    for r in resultats:
        print(f"{r['id']} — {'OK' if r['ok'] else 'À revoir'}")
        if isinstance(r["message"], dict):
            for cle, resultat in r["message"].items():
                if isinstance(resultat, dict):
                    print(f"  {cle} :")
                    for champ, ecart in resultat.items():
                        print(
                            f"    {champ} : attendu {ecart['attendu']!r} ; obtenu {ecart['obtenu']!r}"
                        )
                else:
                    print(f"  {cle} : {resultat}")
        else:
            print(r["message"])
        if r.get("non_verifiees"):
            print("  Étapes non vérifiées : " + ", ".join(r["non_verifiees"]))
    if args.rapport:
        args.rapport.parent.mkdir(parents=True, exist_ok=True)
        args.rapport.write_text(json.dumps(resultats, ensure_ascii=False, indent=2))
    return 0 if all(r["ok"] for r in resultats) else 1


if __name__ == "__main__":
    raise SystemExit(main())
