"""Logistique fournie : sorties isolées et bilan lisible des ateliers."""

import json
import os
import tempfile
from pathlib import Path

from admin_tools.chemins import RACINE


def dossier_tp(numero):
    choisi = os.environ.get("PYX_DOSSIER")
    if choisi:
        dossier = Path(choisi)
        dossier.mkdir(parents=True, exist_ok=True)
        return dossier
    parent = RACINE / "sorties" / numero
    parent.mkdir(parents=True, exist_ok=True)
    return Path(tempfile.mkdtemp(prefix="essai-", dir=parent))


def preparer_etape(dossier, nom):
    """Un sous-dossier par étape, à l'intérieur du même essai de TP."""
    etape = dossier / nom
    etape.mkdir(parents=True, exist_ok=True)
    return etape


def terminer(resultat, dossier, principal=None):
    valeur = resultat.get(principal) if resultat is not None and principal else resultat
    termine = valeur is not None and (
        not isinstance(valeur, dict) or all(v is not None for v in valeur.values())
    )
    bilan = {"termine": termine, "resultat": resultat}
    (dossier / "bilan.json").write_text(
        json.dumps(bilan, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    if not termine:
        print("À compléter : suivez les consignes de l'énoncé, puis relancez ce fichier.")
    if resultat is not None:
        print(json.dumps(resultat, ensure_ascii=False, indent=2))
    print(f"Résultats : {dossier}")
