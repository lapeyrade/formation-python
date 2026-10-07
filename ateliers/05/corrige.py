"""TP05 — Enrichir et conserver les rapports du SI. Voir README.md dans ce dossier.

Un seul script et un seul bilan. Les blocs guidés préparent la production principale.
"""

import tarfile
import zipfile
from pathlib import Path

from admin_tools.atelier import dossier_tp, preparer_etape, terminer
from admin_tools.chemins import DONNEES
from admin_tools.labo import serveur_http
from admin_tools.pilotes import collecter_html
from admin_tools.rapports import importer_csv, lire_alertes
from admin_tools.services import archiver, geolocaliser

dossier_tp_racine = dossier_tp("tp05")
resultats_tp = {}

# === SQLITE — Importer un CSV dans SQLite (30 min) ===
dossier = preparer_etape(dossier_tp_racine, "sqlite")
resultat = None

# Voir rapports.py : validation, création exclusive, transaction et fermeture.
base = dossier / "incidents.sqlite"
importe = importer_csv(DONNEES / "rapport_complet.csv", base)
alertes = lire_alertes(base, 2)
try:
    importer_csv(DONNEES / "rapport_complet.csv", base)
# Une seconde importation ne doit ni écraser la base ni doubler les incidents.
except FileExistsError:
    doublon_refuse = True
resultat = {
    "importees": importe,
    "alertes": len(alertes),
    "echecs_alertes": int(alertes["echecs"].sum()),
    "base_existante_refusee": doublon_refuse,
}

resultats_tp["sqlite"] = resultat

# === API — API et géolocalisation (30 min) ===
dossier = preparer_etape(dossier_tp_racine, "api")
resultat = None

# Même contrat de résultat pour succès, absence et erreur : la boucle peut continuer.
with serveur_http() as url:
    reponses = [
        geolocaliser("8.8.8.8", url + route)
        for route in ["/geo", "/absent", "/invalide", "/erreur"]
    ]
resultat = {
    "statuts": [r["statut"] for r in reponses],
    "source": reponses[0]["source"],
    "pays_simule": reponses[0]["pays"],
}

resultats_tp["api"] = resultat

# === SCRAPY — Extraire une page avec Scrapy (25 min) ===
dossier = preparer_etape(dossier_tp_racine, "scrapy")
resultat = None

# Le spider corrigé extrait les champs ; le pilote gère uniquement son exécution.
resultat = collecter_html(Path(__file__).with_name("spider_corrige.py"), dossier)

resultats_tp["scrapy"] = resultat

# === ARCHIVES — Archives contrôlées (15 min) ===
dossier = preparer_etape(dossier_tp_racine, "archives")
resultat = None

fichiers = [DONNEES / "rapport_complet.csv", DONNEES / "rapport_complet.xlsx"]
z = archiver(fichiers, dossier / "rapport.zip")
t = archiver(fichiers, dossier / "rapport.tar.gz")
# Ouvrir l’archive prouve son contenu : son existence seule ne suffit pas.
with zipfile.ZipFile(z) as archive:
    noms_zip = archive.namelist()
    identiques = all(archive.read(p.name) == p.read_bytes() for p in fichiers)
with tarfile.open(t) as archive:
    noms_tar = archive.getnames()
resultat = {
    "membres": noms_zip,
    "memes_membres": noms_zip == noms_tar,
    "octets_identiques": identiques,
}

resultats_tp["archives"] = resultat

terminer(resultats_tp, dossier_tp_racine, principal="sqlite")
