"""TP04 — Analyser un incident SSH et Web. Voir README.md dans ce dossier.

Un seul script et un seul bilan. Les blocs guidés préparent la production principale.
"""

from pathlib import Path

import pandas as pd

from admin_tools.atelier import dossier_tp, preparer_etape, terminer
from admin_tools.chemins import DONNEES
from admin_tools.metier import analyser_logs, analyser_web
from admin_tools.pilotes import verifier_arguments
from admin_tools.rapports import exporter, rapprocher

dossier_tp_racine = dossier_tp("tp04")
resultats_tp = {}

# === LOGS — Analyser des logs (40 min) ===
dossier = preparer_etape(dossier_tp_racine, "logs")
resultat = None

# Motif, lecture et validation complets : src/admin_tools/metier.py.
bilan = analyser_logs(DONNEES / "auth.log")
# Le seuil sert à sélectionner les alertes, sans retirer les autres compteurs.
alertes = {ip: n for ip, n in bilan["compteurs"].items() if n >= 2}
resultat = {
    "compteurs": bilan["compteurs"],
    "valides": bilan["valides"],
    "succes": bilan["succes"],
    "rejets": len(bilan["rejets"]),
    "alertes": alertes,
}

resultat["web"] = analyser_web(DONNEES / "access.log")
resultats_tp["logs"] = resultat

# === ARGUMENTS — Arguments de commande (15 min) ===
dossier = preparer_etape(dossier_tp_racine, "arguments")
resultat = None

# Compléter le parseur dans cli_corrige.py ; les essais sont fournis.
resultat = verifier_arguments(Path(__file__).with_name("cli_corrige.py"), dossier)

resultats_tp["arguments"] = resultat

# === PANDAS — CSV et Excel avec Pandas (20 min) ===
dossier = preparer_etape(dossier_tp_racine, "pandas")
resultat = None

# Une IP est un identifiant : la conserver en texte évite une conversion numérique.
csv = pd.read_csv(DONNEES / "inventaire.csv", dtype={"ip": str})
xlsx = pd.read_excel(DONNEES / "inventaire.xlsx", dtype={"ip": str})
variante = pd.read_csv(DONNEES / "inventaire_site_manquant.csv", dtype={"ip": str})
variante["site"] = variante["site"].fillna("inconnu")
variante.to_excel(dossier / "nettoye.xlsx", index=False)
# Relire la sortie vérifie ce qui a réellement été enregistré, pas seulement la table.
relue = pd.read_excel(dossier / "nettoye.xlsx")
resultat = {
    "lignes": len(csv),
    "formats_identiques": csv.equals(xlsx),
    "sites_reference": csv.groupby("site").size().to_dict(),
    "inconnus_variante": int((relue["site"] == "inconnu").sum()),
    "colonnes": list(relue.columns),
}

resultats_tp["pandas"] = resultat

# === RAPPORT — Rapport complet et alertes (25 min) ===
dossier = preparer_etape(dossier_tp_racine, "rapport")
resultat = None

compteurs = analyser_logs(DONNEES / "auth.log")["compteurs"]
inventaire = pd.read_csv(DONNEES / "inventaire.csv", dtype={"ip": str})
# La jointure complète est lisible dans src/admin_tools/rapports.py.
# La jointure part des logs pour garder les IP inconnues de l’inventaire.
rapport = rapprocher(compteurs, inventaire)
exporter(rapport, dossier)
alertes = rapport[rapport["echecs"] >= 2]
# Un nom distinct préserve le rapport complet ; le filtre ne doit pas l’écraser.
exporter(alertes, dossier, "alertes")
resultat = {
    "lignes": len(rapport),
    "echecs": int(rapport["echecs"].sum()),
    "inconnus": int((rapport["nom"] == "inconnu").sum()),
    "alertes": len(alertes),
    "echecs_alertes": int(alertes["echecs"].sum()),
}

resultats_tp["rapport"] = resultat

terminer(resultats_tp, dossier_tp_racine, principal="rapport")
