"""Collecte étudiante puis aperçu, application et vérification Ansible natif."""

import csv
import json
import os
import re
import shlex
import socket
import subprocess

from admin_tools.chemins import RACINE
from admin_tools.configuration import PARAMETRES, contenu_configuration, valider_parametres
from admin_tools.distant import charger_inventaire, collecter, connexion
from admin_tools.journal import journal_execution
from admin_tools.logs_distants import telecharger_logs
from admin_tools.systeme import lire_collecte


def recapitulatif(sortie, noms):
    motif = r"^(\S+)\s*:\s*ok=(\d+)\s+changed=(\d+)\s+unreachable=(\d+)\s+failed=(\d+)"
    resultats = {
        nom: dict(zip(["ok", "changed", "unreachable", "failed"], map(int, valeurs), strict=True))
        for nom, *valeurs in re.findall(motif, sortie, re.M)
    }
    if set(resultats) != set(noms) or any(
        r["failed"] or r["unreachable"] for r in resultats.values()
    ):
        raise ValueError("Le récapitulatif Ansible ne confirme pas toutes les cibles.")
    return resultats


def executer(dossier, collecteur=collecter, parametres=None, collecte_seule=False):
    with journal_execution(dossier) as journal:
        return executer_collecte(
            dossier,
            collecteur,
            journal,
            valider_parametres(PARAMETRES if parametres is None else parametres),
            collecte_seule,
        )


def executer_collecte(dossier, collecteur, journal, parametres, collecte_seule=False):
    inventaire = charger_inventaire()
    noms = [c["nom"] for c in inventaire["cibles"]]
    machines = collecteur(inventaire["cibles"], inventaire)
    if not isinstance(machines, list) or len(machines) != len(noms):
        raise ValueError(
            "Compléter collecter_parc : une liste avec une ligne par cible est attendue."
        )
    for mesure in machines:
        fonction = journal.info if mesure["statut"] == "ok" else journal.error
        fonction(
            "statut=%s erreur=%s",
            mesure["statut"],
            mesure["erreur"],
            extra={"etape": "collecte", "cible": mesure["cible"]},
        )
    with (dossier / "collecte.csv").open("w", newline="", encoding="utf-8") as fichier:
        writer = csv.DictWriter(fichier, fieldnames=list(machines[0]))
        writer.writeheader()
        writer.writerows(machines)
    if any(m["statut"] != "ok" for m in machines):
        raise RuntimeError("Collecte partielle conservée dans collecte.csv ; examiner les erreurs.")
    # Un port réservé sans serveur produit un échec contrôlé sur ce poste.
    with socket.socket() as port_ferme:
        port_ferme.bind(("127.0.0.1", 0))
        indisponible = {
            **inventaire["cibles"][0],
            "nom": "cible_indisponible",
            "hote": "127.0.0.1",
            "port": port_ferme.getsockname()[1],
        }
        partiel = collecteur([inventaire["cibles"][0], indisponible], inventaire)
    for mesure in partiel:
        fonction = journal.info if mesure["statut"] == "ok" else journal.error
        fonction(
            "essai contrôlé statut=%s",
            mesure["statut"],
            extra={"etape": "echec_partiel", "cible": mesure["cible"]},
        )
    (dossier / "collecte-partielle.json").write_text(
        json.dumps(partiel, indent=2), encoding="utf-8"
    )
    # Premier point de contrôle : observer et conserver les erreurs, sans
    # lancer Ansible ni préparer de fichier sur les cibles.
    lire_collecte(dossier / "collecte.csv", noms)
    bilan_collecte = {
        "cibles_attendues": [m["cible"] for m in machines] == noms,
        "systemes_linux": all(m["systeme"] == "Linux" for m in machines),
        "disques_valides": all(0 <= m["disque_utilise_pct"] <= 100 for m in machines),
        "echec_partiel_visible": [m["statut"] for m in partiel] == ["ok", "erreur"],
    }
    (dossier / "preuve-collecte.json").write_text(
        json.dumps(bilan_collecte, indent=2), encoding="utf-8"
    )
    if not all(bilan_collecte.values()):
        raise ValueError("Corriger la collecte avant de passer à la configuration.")
    if collecte_seule:
        return bilan_collecte
    variables = {
        **parametres,
        "ansible_ssh_private_key_file": inventaire["cle"],
        "ansible_ssh_common_args": f"-o UserKnownHostsFile={shlex.quote(inventaire['known_hosts'])} -o IdentitiesOnly=yes -o StrictHostKeyChecking=yes",
    }
    hote_ansible = {
        cible["nom"]: {
            "ansible_host": cible["hote"],
            "ansible_port": cible["port"],
            "ansible_user": cible["utilisateur"],
            "ansible_python_interpreter": cible["python"],
            "dossier_tp": cible["dossier_tp"],
        }
        for cible in inventaire["cibles"]
    }
    fichier_inventaire = dossier / "inventaire-ansible.json"
    fichier_inventaire.write_text(
        json.dumps({"all": {"hosts": hote_ansible, "vars": variables}}, indent=2)
    )
    env = {
        **os.environ,
        "ANSIBLE_CONFIG": str(RACINE / "laboratoire/ansible.cfg"),
        "ANSIBLE_NOCOLOR": "1",
        "ANSIBLE_STDOUT_CALLBACK": "default",
    }

    def passage(nom, options=()):
        resultat = subprocess.run(
            [
                "ansible-playbook",
                "-i",
                str(fichier_inventaire),
                str(RACINE / "laboratoire/rapport.yml"),
                *options,
            ],
            env=env,
            capture_output=True,
            text=True,
            check=True,
            timeout=60,
        )
        if any(m in resultat.stdout + resultat.stderr for m in ("[WARNING]", "[ERROR]")):
            raise RuntimeError(resultat.stdout + resultat.stderr)
        (dossier / f"ansible-{nom}.txt").write_text(resultat.stdout, encoding="utf-8")
        journal.info("passage=%s", nom, extra={"etape": "ansible", "cible": "parc"})
        return recapitulatif(resultat.stdout, noms)

    # Préparer uniquement le dossier avant de simuler la copie ; un dossier absent
    # simulé ne suffirait pas au module copy pour vérifier sa destination.
    passage("preparation", ["--tags", "preparation"])
    passage("scripts", ["--tags", "scripts"])
    scripts = []
    for cible in inventaire["cibles"]:
        with connexion(cible, inventaire) as client:
            contenu = client.run(
                "cat -- " + shlex.quote(cible["dossier_tp"] + "/preuve-script.json"),
                hide=True,
                timeout=3,
                in_stream=False,
            ).stdout
        scripts.append({"cible": cible["nom"], **json.loads(contenu)})
    if [(s["cible"], s["hostname"], s["systeme"]) for s in scripts] != [
        (m["cible"], m["hostname"], m["systeme"]) for m in machines
    ]:
        raise ValueError("Le script distant ne confirme pas les identités collectées.")
    (dossier / "preuve-scripts.json").write_text(json.dumps(scripts, indent=2), encoding="utf-8")
    logs = telecharger_logs(inventaire["cibles"], inventaire, dossier, journal)
    avant = [lire_configuration(c, inventaire) for c in inventaire["cibles"]]
    apercu = passage("apercu", ["--check", "--diff", "--tags", "configuration"])
    apres = [lire_configuration(c, inventaire) for c in inventaire["cibles"]]
    if avant != apres:
        raise RuntimeError("La prévisualisation a modifié la configuration.")
    premier = passage("premier")
    second = passage("second")
    fichiers = [lire_configuration(c, inventaire) for c in inventaire["cibles"]]
    preuve = {
        "cibles": noms,
        "parametres": parametres,
        "apercu": apercu,
        "avant_apercu": avant,
        "apres_apercu": apres,
        "premier": premier,
        "second": second,
        "fichiers": fichiers,
    }
    (dossier / "preuve-ansible.json").write_text(
        json.dumps(preuve, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return {
        **bilan_collecte,
        "apercu_sans_modification": avant == apres,
        "premier_reussi": all(r["ok"] >= 2 for r in premier.values()),
        "second_sans_changement": all(r["changed"] == 0 for r in second.values()),
        "contenus_conformes": all(
            f["contenu"] == contenu_configuration(f["cible"], parametres) for f in fichiers
        ),
        "permissions_conformes": all(f["mode"] == "0640" for f in fichiers),
        "logs_telecharges": len(logs["sources"]),
        "evenements_logs": logs["analyse"]["valides"],
        "echecs_logs": sum(logs["analyse"]["compteurs"].values()),
        "scripts_executes": len(scripts),
    }


def lire_configuration(cible, inventaire):
    """Lire la preuve sur la cible, indépendamment du récapitulatif Ansible."""
    chemin = cible["dossier_tp"] + "/supervision.ini"
    with connexion(cible, inventaire) as client:
        existe = client.run(
            "test -f " + shlex.quote(chemin), hide=True, timeout=3, in_stream=False, warn=True
        )
        if existe.exited == 1:
            return {
                "cible": cible["nom"],
                "chemin": chemin,
                "statut": "absent",
                "contenu": None,
                "mode": None,
            }
        if existe.exited != 0:
            raise RuntimeError("Impossible de vérifier la configuration distante.")
        contenu = client.run(
            "cat -- " + shlex.quote(chemin), hide=True, timeout=3, in_stream=False
        ).stdout
        mode = (
            client.run(
                "stat -c %a -- " + shlex.quote(chemin), hide=True, timeout=3, in_stream=False
            )
            .stdout.strip()
            .zfill(4)
        )
    return {
        "cible": cible["nom"],
        "chemin": chemin,
        "statut": "present",
        "contenu": contenu,
        "mode": mode,
    }
