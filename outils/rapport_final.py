"""Exécuter le scénario final avec paramètres et SMTP local de capture."""

import argparse
import json
import smtplib
import sqlite3
import sys
from pathlib import Path

from admin_tools.journal import journal_execution
from admin_tools.labo import serveur_smtp
from admin_tools.metier import positif
from admin_tools.rapports import exporter, importer_csv, lire_alertes
from admin_tools.services import archiver, envoyer_archive
from admin_tools.systeme import joindre_diagnostic, lire_collecte


def construire_rapport(source, dossier, port, seuil=2, collecte=None):
    if not Path(source).is_file():
        raise FileNotFoundError(f"Source absente : {source}")
    if collecte is not None:
        lire_collecte(collecte)
    dossier = Path(dossier)
    dossier.mkdir(parents=True, exist_ok=False)
    with journal_execution(dossier) as journal:
        journal.info("début du traitement", extra={"etape": "import"})
        importees = importer_csv(source, dossier / "incidents.sqlite")
        alertes = lire_alertes(dossier / "incidents.sqlite", seuil)
        fichiers = exporter(alertes, dossier, "alertes")
        complements = joindre_diagnostic(dossier, collecte)
        archive = archiver([*fichiers, *complements], dossier / "rapport.zip")
        journal.info("archive vérifiée", extra={"etape": "archive"})
        envoyer_archive(archive, port, sujet=f"Rapport PYX : {len(alertes)} alertes")
        journal.info("message soumis au SMTP local", extra={"etape": "smtp"})
        return {
            "importees": importees,
            "alertes": len(alertes),
            "echecs_alertes": int(alertes["echecs"].sum()),
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument(
        "--sortie", type=Path, required=True, help="nouveau dossier, jamais un dossier existant"
    )
    parser.add_argument("--seuil", type=positif, default=2)
    parser.add_argument("--collecte", type=Path, help="CSV de collecte SSH complète à joindre")
    args = parser.parse_args()
    try:
        with serveur_smtp() as (port, capture):
            resultat = construire_rapport(args.source, args.sortie, port, args.seuil, args.collecte)
            (args.sortie / "message.eml").write_bytes(capture.messages[0])
        print(json.dumps(resultat, ensure_ascii=False, indent=2))
        print("Rapport envoyé uniquement au SMTP local de capture.")
    except (OSError, ValueError, sqlite3.Error, smtplib.SMTPException) as erreur:
        print(f"Rapport non terminé : {erreur}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
