"""TP06 — Collecter à distance et diffuser les alertes. Voir README.md dans ce dossier.

Un seul script et un seul bilan. Les blocs guidés préparent la production principale.
"""

import argparse
import zipfile
from email import policy
from email.parser import BytesParser
from pathlib import Path

from distant import executer

from admin_tools.atelier import dossier_tp, preparer_etape, terminer
from admin_tools.chemins import DONNEES
from admin_tools.journal import journal_execution
from admin_tools.labo import serveur_smtp
from admin_tools.rapports import exporter, importer_csv, lire_alertes
from admin_tools.services import archiver, envoyer_archive
from admin_tools.systeme import joindre_diagnostic

parseur = argparse.ArgumentParser(description="TP 06 — rapport et administration distante")
parseur.add_argument("--laboratoire", action="store_true", help="exécuter Fabric et Ansible")
parseur.add_argument("--source", type=Path, default=DONNEES / "rapport_complet.csv")
parseur.add_argument("--collecte", type=Path, help="collecte complète d'un essai précédent")
options = parseur.parse_args()

dossier_tp_racine = dossier_tp("tp06")
resultats_tp = {}

# === EMAIL — Message et pièce jointe (15 min) ===
dossier = preparer_etape(dossier_tp_racine, "email")
resultat = None

archive = archiver([DONNEES / "rapport_complet.csv"], dossier / "rapport.zip")
with serveur_smtp() as (port, capture):
    envoyer_archive(archive, port, sujet="Rapport PYX : 2 alertes")
    brut = capture.messages[0]
(dossier / "message.eml").write_bytes(brut)
# Analyser le message capturé vérifie aussi la pièce jointe réellement transmise.
message = BytesParser(policy=policy.default).parsebytes(brut)
pieces = list(message.iter_attachments())
resultat = {
    "messages": 1,
    "objet": message["Subject"],
    "piece_jointe": pieces[0].get_filename(),
    "octets_identiques": pieces[0].get_payload(decode=True) == archive.read_bytes(),
}

resultats_tp["email"] = resultat

# === DISTANT — Fabric et Ansible sur la VM (40 min) ===
dossier = preparer_etape(dossier_tp_racine, "distant")
resultat = None

# Les cibles SSH de l'inventaire sont préparées avant ce créneau.
if options.laboratoire:
    from solution_collecte import collecter_parc

    resultat = executer(dossier, collecter_parc)
else:
    print("Étape distante non exécutée : relancer avec --laboratoire après préparation.")

resultats_tp["distant"] = resultat

# === INTEGRATION — Chaîne complète de rapport (15 min) ===
dossier = preparer_etape(dossier_tp_racine, "integration")
resultat = None

with journal_execution(dossier) as journal:
    with serveur_smtp() as (port, capture):
        # L’ordre est essentiel : toute erreur de lecture/export empêche d’atteindre l’envoi.
        journal.info("début du traitement", extra={"etape": "import"})
        importees = importer_csv(options.source, dossier / "incidents.sqlite")
        alertes = lire_alertes(dossier / "incidents.sqlite", 2)
        # Réutiliser les fonctions testées garde ici le rôle d’assemblage du TP final.
        fichiers = exporter(alertes, dossier, "alertes")
        collecte = (
            dossier_tp_racine / "distant/collecte.csv" if options.laboratoire else options.collecte
        )
        complements = joindre_diagnostic(dossier, collecte)
        archive = archiver([*fichiers, *complements], dossier / "rapport.zip")
        journal.info("archive vérifiée", extra={"etape": "archive"})
        envoyer_archive(archive, port, sujet=f"Rapport PYX : {len(alertes)} alertes")
        (dossier / "message.eml").write_bytes(capture.messages[0])
        nombre_messages = len(capture.messages)
        journal.info("message soumis au SMTP local", extra={"etape": "smtp"})
# Contrôler les membres de l’archive évite d’expédier un fichier en trop ou manquant.
with zipfile.ZipFile(archive) as fichier:
    membres = fichier.namelist()
resultat = {
    "importees": importees,
    "alertes": len(alertes),
    "echecs_alertes": int(alertes["echecs"].sum()),
    "rapport_archive": set(["alertes.csv", "alertes.xlsx"]) <= set(membres),
    "diagnostic_archive": "diagnostic.json" in membres,
    "collecte_archivee_si_executee": (collecte is not None) == ("collecte.csv" in membres),
    "messages": nombre_messages,
}

resultats_tp["integration"] = resultat

terminer(resultats_tp, dossier_tp_racine, principal="integration")
