"""Enrichir le rapport : compléter les TODO ; services de test et sorties sont fournis."""

import sqlite3
import tarfile
import zipfile
from pathlib import Path

import pandas as pd
import requests

from admin_tools.atelier import dossier_tp, preparer_etape, terminer
from admin_tools.chemins import DONNEES
from admin_tools.labo import serveur_http
from admin_tools.pilotes import collecter_html
from admin_tools.services import archiver

dossier_tp_racine = dossier_tp("tp05")
resultats_tp = {}

# === SQLITE — Importer un CSV dans SQLite (30 min) ===
dossier = preparer_etape(dossier_tp_racine, "sqlite")
source = DONNEES / "rapport_complet.csv"
base = dossier / "incidents.sqlite"
rapport = pd.read_csv(source, dtype={"ip": str, "nom": str, "site": str})
# Fourni : un rapport invalide ne doit pas ouvrir une transaction d'import.
if list(rapport.columns) != ["ip", "nom", "site", "echecs"] or rapport.isna().any().any():
    raise ValueError("Colonnes ou données du rapport incorrectes.")
if rapport["ip"].duplicated().any():
    raise ValueError("IP dupliquée dans le rapport.")
if not pd.api.types.is_integer_dtype(rapport["echecs"]) or (rapport["echecs"] < 0).any():
    raise ValueError("Les échecs doivent être des entiers positifs ou nuls.")
with base.open("xb"):
    pass  # Réserver une base neuve ; un second essai utilise un autre dossier.
connexion = sqlite3.connect(base)
try:
    with connexion:  # Fourni : validation de transaction ou rollback en cas d'exception.
        connexion.execute(
            "CREATE TABLE incidents (ip TEXT PRIMARY KEY, nom TEXT, site TEXT, echecs INTEGER)"
        )
        requete: str | None = None  # TODO 1 : INSERT INTO incidents VALUES (?, ?, ?, ?).
        if requete is not None:
            # Les valeurs restent des paramètres, jamais une concaténation SQL.
            connexion.executemany(requete, rapport.itertuples(index=False, name=None))
    nombre = connexion.execute("SELECT COUNT(*) FROM incidents").fetchone()[0]
    alertes = connexion.execute(
        "SELECT ip, nom, site, echecs FROM incidents WHERE echecs >= ? ORDER BY ip", (2,)
    ).fetchall()
finally:
    connexion.close()  # Le contexte transactionnel ne ferme pas la connexion.
doublon_refuse = False
try:
    with base.open("xb"):
        pass
except FileExistsError:
    doublon_refuse = True
resultat = {
    "importees": None,  # TODO 2 : utiliser nombre, obtenu par SELECT, pas la taille du CSV.
    "alertes": len(alertes),
    "echecs_alertes": sum(ligne[3] for ligne in alertes),
    "base_existante_refusee": doublon_refuse,
}
resultats_tp["sqlite"] = resultat

# === API — API et géolocalisation (30 min) ===
dossier = preparer_etape(dossier_tp_racine, "api")


def localiser(ip, url):
    sortie = {
        "ip": ip,
        "pays": None,
        "ville": None,
        "statut": "erreur",
        "source": "simulation_locale",
    }
    try:
        reponse = requests.get(url, params={"ip": ip}, timeout=3)
        reponse.raise_for_status()  # Vérifier HTTP AVANT de décoder le corps.
        contenu = reponse.json()
        if not isinstance(contenu, dict):
            return sortie
        if contenu.get("status") == "fail":
            # TODO 1 : changer le statut en "indisponible" ; ce n'est pas une erreur HTTP.
            pass
        elif contenu.get("status") == "success" and contenu.get("country"):
            # TODO 2 : renseigner pays/ville et le statut "localisee" avec sortie.update(...).
            pass
    except (requests.RequestException, ValueError):
        pass  # Transport, statut HTTP ou décodage : garder explicitement "erreur".
    return sortie


with serveur_http() as url:
    reponses = [
        localiser("8.8.8.8", url + route) for route in ["/geo", "/absent", "/invalide", "/erreur"]
    ]
resultat = {
    "statuts": [r["statut"] for r in reponses],
    "source": reponses[0]["source"],
    "pays_simule": reponses[0]["pays"],
}
resultats_tp["api"] = resultat

# === SCRAPY — Extraire une page avec Scrapy (25 min) ===
dossier = preparer_etape(dossier_tp_racine, "scrapy")
# TODO : trois champs à compléter dans spider.py ; le pilote gère serveur et export JSON.
resultat = collecter_html(Path(__file__).with_name("spider.py"), dossier)
resultats_tp["scrapy"] = resultat

# === ARCHIVES — Archives contrôlées (15 min) ===
dossier = preparer_etape(dossier_tp_racine, "archives")
fichiers = [DONNEES / "rapport_complet.csv", DONNEES / "rapport_complet.xlsx"]
# Fourni : les deux formats réutilisent archiver ; lire sa gestion des noms et modes.
z = archiver(fichiers, dossier / "rapport.zip")
t = archiver(fichiers, dossier / "rapport.tar.gz")
with zipfile.ZipFile(z) as archive:
    noms_zip = archive.namelist()
    identiques = all(archive.read(p.name) == p.read_bytes() for p in fichiers)
with tarfile.open(t) as archive:
    noms_tar = archive.getnames()
resultat = {
    "membres": noms_zip,
    "memes_membres": None,  # TODO 1 : comparer noms_zip et noms_tar.
    "octets_identiques": None,  # TODO 2 : utiliser identiques, issu de la relecture réelle.
}
resultats_tp["archives"] = resultat

terminer(resultats_tp, dossier_tp_racine, principal="sqlite")
