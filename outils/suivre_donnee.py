"""Suivre la même IP des logs jusqu'à la pièce jointe capturée localement."""

import json
import sqlite3
import zipfile
from email import policy
from email.parser import BytesParser
from pathlib import Path

import pandas as pd

from admin_tools.atelier import dossier_tp
from admin_tools.chemins import DONNEES
from admin_tools.labo import serveur_smtp
from admin_tools.metier import analyser_logs
from admin_tools.rapports import exporter, importer_csv, lire_alertes, rapprocher
from admin_tools.services import archiver, envoyer_archive

IP_SUIVIE = "192.0.2.1"


def construire_trace(dossier):
    dossier = Path(dossier)
    dossier.mkdir(parents=True, exist_ok=True)
    analyse = analyser_logs(DONNEES / "auth.log")
    inventaire = pd.read_csv(DONNEES / "inventaire.csv", dtype={"ip": str})
    rapport = rapprocher(analyse["compteurs"], inventaire)
    csv, _ = exporter(rapport, dossier)
    base = dossier / "incidents.sqlite"
    importer_csv(csv, base)
    connexion = sqlite3.connect(base.resolve().as_uri() + "?mode=ro", uri=True)
    try:
        ligne = connexion.execute(
            "SELECT ip, nom, site, echecs FROM incidents WHERE ip = ?", (IP_SUIVIE,)
        ).fetchone()
    finally:
        connexion.close()
    alertes = lire_alertes(base, 2)
    fichiers = exporter(alertes, dossier, "alertes")
    archive = archiver(fichiers, dossier / "rapport.zip")
    with serveur_smtp() as (port, capture):
        envoyer_archive(archive, port, sujet=f"Rapport PYX : {len(alertes)} alertes")
        brut = capture.messages[0]
        nombre = len(capture.messages)
    (dossier / "message.eml").write_bytes(brut)
    message = BytesParser(policy=policy.default).parsebytes(brut)
    piece = next(message.iter_attachments())
    ligne_rapport = rapport.loc[rapport["ip"] == IP_SUIVIE].to_dict("records")[0]
    with zipfile.ZipFile(archive) as contenu:
        membres = contenu.namelist()
        csv_archive = contenu.read("alertes.csv")
    preuve = {
        "ip_source": IP_SUIVIE,
        "cible_du_log": "srv-bastion",
        "compteur_echecs": analyse["compteurs"][IP_SUIVIE],
        "rapport_complet": ligne_rapport,
        "sqlite": dict(zip(["ip", "nom", "site", "echecs"], ligne, strict=True)),
        "seuil": 2,
        "alertes": alertes.to_dict("records"),
        "zip": membres,
        "csv_archive_identique": csv_archive == fichiers[0].read_bytes(),
        "smtp": {
            "messages": nombre,
            "objet": message["Subject"],
            "piece_jointe": piece.get_filename(),
            "octets_identiques": piece.get_payload(decode=True) == archive.read_bytes(),
        },
        "limite": "Une IP source et un seuil ne prouvent pas une intrusion.",
    }
    (dossier / "trace.json").write_text(
        json.dumps(preuve, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return preuve


def main():
    dossier = dossier_tp("fil-donnee")
    preuve = construire_trace(dossier)
    print(json.dumps(preuve, ensure_ascii=False, indent=2))
    print(f"Lire trace.json et comparer les fichiers : {dossier}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
