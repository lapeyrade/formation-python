"""TP06 — Collecter à distance et diffuser les alertes. Voir README.md dans ce dossier.

Un seul script et un seul bilan. Les blocs guidés préparent la production principale.
"""

import argparse
import zipfile
from email import policy
from email.parser import BytesParser
from pathlib import Path

from distant import executer
from mes_fonctions import (
    archiver,
    envoyer_archive,
    exporter,
    importer_csv,
    lire_alertes,
)

from admin_tools.atelier import dossier_tp, preparer_etape, terminer
from admin_tools.chemins import DONNEES
from admin_tools.journal import journal_execution
from admin_tools.labo import serveur_smtp
from admin_tools.systeme import joindre_diagnostic

parseur = argparse.ArgumentParser(description="TP 06 — rapport et administration distante")
parseur.add_argument("--laboratoire", action="store_true", help="exécuter Fabric et Ansible")
parseur.add_argument("--source", type=Path, default=DONNEES / "rapport_complet.csv")
parseur.add_argument("--collecte", type=Path, help="collecte complète d'un essai précédent")
options = parseur.parse_args()

dossier_tp_racine = dossier_tp("tp06")
resultats_tp = {}

# === EMAIL — Message et pièce jointe (15 min) ===
# CONSIGNE : Adapter le sujet et contrôler la pièce reçue.
# FICHIER : depart.py. Voir README.md, section email.
dossier = preparer_etape(dossier_tp_racine, "email")
resultat = None

# Fourni : le message est envoyé seulement au SMTP local de capture, jamais à une boîte réelle.
archive = archiver([DONNEES / "rapport_complet.csv"], dossier / "rapport.zip")
with serveur_smtp() as (port, capture):
    # TODO 1 : adapter le sujet pour obtenir "Rapport PYX : 2 alertes".
    envoyer_archive(archive, port, sujet="À compléter")
    brut = capture.messages[0]
(dossier / "message.eml").write_bytes(brut)
message = BytesParser(policy=policy.default).parsebytes(brut)
pieces = list(message.iter_attachments())
resultat = {
    "messages": len(capture.messages),
    "objet": message["Subject"],
    "piece_jointe": pieces[0].get_filename(),
    "octets_identiques": None,  # TODO 2 : comparer get_payload(decode=True) et archive.read_bytes().
}

resultats_tp["email"] = resultat

# === DISTANT — Fabric et Ansible sur la VM (40 min) ===
# CONSIGNE : Une extraction disque, puis des manipulations guidées.
# FICHIER : mes_collectes.py. Voir README.md, section distant.
dossier = preparer_etape(dossier_tp_racine, "distant")
resultat = None

# Les cibles SSH de l'inventaire sont préparées avant ce créneau.
if options.laboratoire:
    from mes_collectes import collecter_parc

    resultat = executer(dossier, collecter_parc)
else:
    print("Étape distante non exécutée : relancer avec --laboratoire après préparation.")

resultats_tp["distant"] = resultat

# === INTEGRATION — Chaîne complète de rapport (15 min) ===
# CONSIGNE : Assembler l’archive, envoyer puis compter.
# FICHIER : depart.py. Voir README.md, section integration.
dossier = preparer_etape(dossier_tp_racine, "integration")
resultat = None

source = options.source
base = dossier / "incidents.sqlite"
collecte = dossier_tp_racine / "distant/collecte.csv" if options.laboratoire else options.collecte
# Fourni : les fonctions précédentes sont réutilisées ; aucune réécriture au TP final.
# Le diagnostic et la collecte sont validés avant de préparer la diffusion.
with journal_execution(dossier) as journal:
    journal.info("début du traitement", extra={"etape": "import"})
    importees = importer_csv(source, base)
    alertes = lire_alertes(base, 2)
    fichiers = exporter(alertes, dossier, "alertes")
    complements = joindre_diagnostic(dossier, collecte)
    # TODO 1 : remplacer None par archiver([*fichiers, *complements], dossier / "rapport.zip").
    archive = None
    nombre_messages = 0
    membres = []
    if archive is not None:  # Garde du squelette ; compléter l'archive pour entrer ici.
        with zipfile.ZipFile(archive) as fichier:
            membres = fichier.namelist()
        journal.info("archive vérifiée", extra={"etape": "archive"})
        with serveur_smtp() as (port, capture):
            # TODO 2 : appeler envoyer_archive avec le sujet calculé selon len(alertes).
            # L'envoi arrive seulement après toutes les étapes réussies.
            if capture.messages:
                (dossier / "message.eml").write_bytes(capture.messages[0])
                nombre_messages = len(capture.messages)
                journal.info("message soumis au SMTP local", extra={"etape": "smtp"})
resultat = {
    "importees": importees,
    "alertes": len(alertes),
    "echecs_alertes": int(alertes["echecs"].sum()),
    "rapport_archive": {"alertes.csv", "alertes.xlsx"} <= set(membres),
    "diagnostic_archive": "diagnostic.json" in membres,
    "collecte_archivee_si_executee": (collecte is not None) == ("collecte.csv" in membres),
    "messages": None,  # TODO 3 : utiliser nombre_messages, relu depuis le SMTP de capture.
}

resultats_tp["integration"] = resultat

terminer(resultats_tp, dossier_tp_racine, principal="integration")
