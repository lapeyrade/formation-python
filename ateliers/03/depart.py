"""TP03 — Préparer un adressage et diagnostiquer un hôte. Voir README.md dans ce dossier.

Un seul script et un seul bilan. Les blocs guidés préparent la production principale.
"""

import json
import sys
from pathlib import Path

from admin_tools.atelier import dossier_tp, preparer_etape, terminer
from admin_tools.chemins import RACINE
from admin_tools.journal import journal_execution
from admin_tools.pilotes import clients_bibliotheque
from admin_tools.systeme import collecter_local, enregistrer, lancer
from ma_boite.modeles import Machine
from ma_boite.reseau import generer_ips

dossier_tp_racine = dossier_tp("tp03")
resultats_tp = {}

# === GENERATEUR — Générateur d’IP (30 min) ===
dossier = preparer_etape(dossier_tp_racine, "generateur")
resultat = None

g = generer_ips("192.0.2.0/29")
premiere = list(g)
seconde = list(g)
nouvelle = list(generer_ips("192.0.2.0/29"))
resultat = {"adresses": premiere, "longueurs": [len(premiere), len(seconde), len(nouvelle)]}
resultat["candidates"] = list(generer_ips("192.0.2.0/29", ["192.0.2.1", "192.0.2.3"], 3))

resultats_tp["generateur"] = resultat

# === CLASSE — Classe Machine (20 min) ===
dossier = preparer_etape(dossier_tp_racine, "classe")
resultat = None

a = Machine("alpha", "192.0.2.1")
b = Machine("beta", "192.0.2.2")
b.actif = False
resultat = {"resumes": [a.resume(), b.resume()], "alpha_active": a.actif}

resultats_tp["classe"] = resultat

# === BIBLIOTHEQUE — Bibliothèque et deux clients (15 min) ===
dossier = preparer_etape(dossier_tp_racine, "bibliotheque")
resultat = None

ips = list(generer_ips("192.0.2.0/29"))
machines = [Machine(f"h{i}", ip) for i, ip in enumerate(ips, 1)]
# Les deux clients utilisent exactement le même package que ce script.
clients = Path(__file__).parent
resultat = clients_bibliotheque(clients, dossier, ips, machines)

resultats_tp["bibliotheque"] = resultat

# === DIAGNOSTIC — Diagnostic de la machine (35 min) ===
dossier = preparer_etape(dossier_tp_racine, "diagnostic")
# Fourni : la collecte est locale et en lecture seule ; ses valeurs varient par poste.
with journal_execution(dossier) as journal:
    rapport = collecter_local(dossier)
    enregistrer(rapport, dossier)
    journal.info(
        "observations conservées", extra={"etape": "diagnostic", "cible": rapport["hostname"]}
    )
    interpretations = {}
    for nom, observation in rapport["observations_linux"].items():
        print("Source à interpréter :", nom, observation)
        # TODO 1 : rédiger une conclusion limitée et une prochaine action pour chaque source.
        # Lire statut avant de conclure : une source inaccessible signifie état inconnu.
        interpretations[nom] = {"observation": observation, "conclusion": "", "action": ""}
    (dossier / "interpretation.json").write_text(
        json.dumps(interpretations, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    # Fourni : ces commandes enfant rendent échec et délai reproductibles sans toucher un service.
    commande = [sys.executable, str(RACINE / "outils/commande_enfant.py")]
    echec = lancer(commande + ["echec"])
    attente = lancer(commande + ["attente"], timeout=0.1)
    resultat = {
        "identite": bool(rapport["hostname"] and rapport["systeme"]),
        "disque_coherent": 0 <= rapport["disque_libre"] <= rapport["disque_total"],
        "commande_reussie": rapport["execution"]["statut"] == "ok",
        "code_echec": echec["code"],
        "delai_depasse": attente["statut"] == "timeout",
        "contexte_complet": bool(
            rapport["date_utc"] and rapport["utilisateur"] and rapport["chemin_mesure"]
        ),
        "commandes_systeme_reussies": all(
            execution is None or execution["statut"] == "ok"
            for execution in rapport["commandes"].values()
        ),
        # TODO 2 : remplacer None par le contrôle de vos trois interprétations renseignées.
        "observations_interpretees": None,
    }
    journal.error(
        "essai contrôlé : code=%s timeout=%s",
        echec["code"],
        attente["statut"],
        extra={"etape": "commande", "cible": "simulation"},
    )

resultats_tp["diagnostic"] = resultat

terminer(resultats_tp, dossier_tp_racine, principal="diagnostic")
