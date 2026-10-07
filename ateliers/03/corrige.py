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
from solution.ma_boite.modeles import Machine
from solution.ma_boite.reseau import generer_ips

dossier_tp_racine = dossier_tp("tp03")
resultats_tp = {}

# === GENERATEUR — Générateur d’IP (30 min) ===
dossier = preparer_etape(dossier_tp_racine, "generateur")
resultat = None

g = generer_ips("192.0.2.0/29")
premiere = list(g)
# g conserve son état : il est épuisé après la première conversion en liste.
seconde = list(g)
# Rappeler la fonction crée un autre générateur, qui repart du premier hôte.
nouvelle = list(generer_ips("192.0.2.0/29"))
resultat = {"adresses": premiere, "longueurs": [len(premiere), len(seconde), len(nouvelle)]}
resultat["candidates"] = list(generer_ips("192.0.2.0/29", ["192.0.2.1", "192.0.2.3"], 3))

resultats_tp["generateur"] = resultat

# === CLASSE — Classe Machine (20 min) ===
dossier = preparer_etape(dossier_tp_racine, "classe")
resultat = None

a = Machine("alpha", "192.0.2.1")
b = Machine("beta", "192.0.2.2")
# actif est un attribut de chaque instance : modifier beta ne change pas alpha.
b.actif = False
resultat = {"resumes": [a.resume(), b.resume()], "alpha_active": a.actif}

resultats_tp["classe"] = resultat

# === BIBLIOTHEQUE — Bibliothèque et deux clients (15 min) ===
dossier = preparer_etape(dossier_tp_racine, "bibliotheque")
resultat = None

ips = list(generer_ips("192.0.2.0/29"))
machines = [Machine(f"h{i}", ip) for i, ip in enumerate(ips, 1)]
# Les deux clients utilisent exactement le même package que ce script.
clients = Path(__file__).parent / "solution"
resultat = clients_bibliotheque(clients, dossier, ips, machines)

resultats_tp["bibliotheque"] = resultat

# === DIAGNOSTIC — Diagnostic de la machine (35 min) ===
dossier = preparer_etape(dossier_tp_racine, "diagnostic")
with journal_execution(dossier) as journal:
    rapport = collecter_local(dossier)
    enregistrer(rapport, dossier)
    journal.info(
        "observations conservées", extra={"etape": "diagnostic", "cible": rapport["hostname"]}
    )
    # Distinguer faits mesurés, conclusions limitées et prochaine observation.
    interpretations = {}
    limites = {
        "memoire": (
            "La disponibilité est mesurée à cet instant, sans preuve de fuite.",
            "Comparer à un relevé ultérieur et aux processus concernés.",
        ),
        "reseau": (
            "Les interfaces et routes décrivent la configuration, sans preuve de connectivité.",
            "Vérifier la route vers la destination de l'intervention.",
        ),
        "services": (
            "Ce sont les unités en échec connues de systemd, pas tous les services.",
            "Examiner le journal d'une unité concernée avant toute action.",
        ),
    }
    for nom, observation in rapport["observations_linux"].items():
        conclusion, action = limites[nom]
        if observation["statut"] != "ok":
            conclusion = "Source indisponible : état du sous-système inconnu."
            action = "Vérifier l'outil, les droits et le contexte de ce poste."
        interpretations[nom] = {
            "observation": observation,
            "conclusion": conclusion,
            "action": action,
        }
    (dossier / "interpretation.json").write_text(
        json.dumps(interpretations, ensure_ascii=False, indent=2)
    )
    # Une commande réelle est complétée par des échecs reproductibles.
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
        "observations_interpretees": len(interpretations) == 3,
        "commandes_systeme_reussies": all(
            execution is None or execution["statut"] == "ok"
            for execution in rapport["commandes"].values()
        ),
    }
    journal.error(
        "essai contrôlé : code=%s timeout=%s",
        echec["code"],
        attente["statut"],
        extra={"etape": "commande", "cible": "simulation"},
    )

resultats_tp["diagnostic"] = resultat

terminer(resultats_tp, dossier_tp_racine, principal="diagnostic")
