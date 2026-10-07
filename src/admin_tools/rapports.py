"""Traitements tabulaires et SQLite ; référence pour les ateliers d'intégration."""

import sqlite3
from pathlib import Path

import pandas as pd

COLONNES = ["ip", "nom", "site", "echecs"]


def rapprocher(compteurs, inventaire):
    if inventaire["ip"].isna().any() or inventaire["ip"].duplicated().any():
        raise ValueError("Les IP de l'inventaire doivent être renseignées et uniques.")
    bilan = pd.DataFrame(list(compteurs.items()), columns=["ip", "echecs"])
    # Une jointure gauche conserve les IP observées, même absentes de l’inventaire.
    # one_to_one interdit les doublons qui multiplieraient artificiellement les lignes.
    rapport = bilan.merge(
        inventaire[["ip", "nom", "site"]], on="ip", how="left", validate="one_to_one"
    )
    rapport[["nom", "site"]] = rapport[["nom", "site"]].fillna("inconnu")
    return rapport[COLONNES].sort_values("ip").reset_index(drop=True)


def exporter(rapport, dossier, nom="rapport_complet"):
    dossier = Path(dossier)
    dossier.mkdir(parents=True, exist_ok=True)
    csv, xlsx = dossier / f"{nom}.csv", dossier / f"{nom}.xlsx"
    # L’index Pandas est technique : l’exporter ajouterait une colonne inutile.
    rapport.to_csv(csv, index=False)
    rapport.to_excel(xlsx, index=False, engine="openpyxl")
    return csv, xlsx


def importer_csv(source, base):
    # Réserver un fichier neuf : ne jamais remplacer une base existante.
    rapport = pd.read_csv(source, dtype={"ip": str, "nom": str, "site": str})
    if list(rapport.columns) != COLONNES or rapport.isna().any().any():
        raise ValueError("Colonnes ou données du rapport incorrectes.")
    if rapport["ip"].duplicated().any():
        raise ValueError("IP dupliquée dans le rapport.")
    if not pd.api.types.is_integer_dtype(rapport["echecs"]) or (rapport["echecs"] < 0).any():
        raise ValueError("Les échecs doivent être des entiers positifs ou nuls.")
    base = Path(base)
    # Le mode exclusif échoue si la base existe déjà : aucun écrasement silencieux.
    with base.open("xb"):
        pass
    connexion = sqlite3.connect(base)
    try:
        # Ce contexte valide la transaction si tout réussit, ou l’annule en cas d’erreur.
        # Il ne ferme pas la connexion : ce rôle revient au finally ci-dessous.
        with connexion:
            connexion.execute(
                "CREATE TABLE incidents (ip TEXT PRIMARY KEY, nom TEXT, site TEXT, echecs INTEGER)"
            )
            # Les ? séparent les valeurs de la syntaxe SQL, même si un nom contient une quote.
            connexion.executemany(
                "INSERT INTO incidents VALUES (?, ?, ?, ?)",
                rapport.itertuples(index=False, name=None),
            )
    finally:
        # Libérer la connexion sur le chemin normal comme en cas d’exception.
        connexion.close()
    return len(rapport)


def lire_alertes(base, seuil=2):
    if seuil < 1:
        raise ValueError("Le seuil doit être positif.")
    # Lecture seule : un chemin inexistant ne doit pas créer une nouvelle base.
    connexion = sqlite3.connect(Path(base).resolve().as_uri() + "?mode=ro", uri=True)
    try:
        lignes = connexion.execute(
            "SELECT ip, nom, site, echecs FROM incidents WHERE echecs >= ? ORDER BY ip", (seuil,)
        ).fetchall()
    finally:
        # Libérer la connexion sur le chemin normal comme en cas d’exception.
        connexion.close()
    return pd.DataFrame(lignes, columns=COLONNES)
