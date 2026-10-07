"""Inventaire commun et collecte SSH : conserver un résultat pour chaque cible."""

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

from fabric import Connection
from invoke.exceptions import CommandTimedOut, UnexpectedExit
from paramiko import RejectPolicy, SSHException

from admin_tools.chemins import RACINE


def charger_inventaire(chemin=None):
    """Les chemins relatifs de clés sont relatifs au fichier d'inventaire."""
    chemin = Path(chemin or os.environ.get("PYX_INVENTAIRE", RACINE / ".labo/inventaire.json"))
    chemin = chemin.expanduser().resolve()
    try:
        inventaire = json.loads(chemin.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError("Inventaire absent : suivre laboratoire/README.md.") from None
    if not isinstance(inventaire, dict):
        raise ValueError("L'inventaire doit être un objet JSON.")
    cibles = inventaire.get("cibles", [])
    if not isinstance(cibles, list) or len(cibles) != 2:
        raise ValueError("Cet exercice demande deux cibles SSH distinctes.")
    noms, adresses = set(), set()
    for cible in cibles:
        if not isinstance(cible, dict):
            raise ValueError("Chaque cible doit être un objet JSON.")
        nom, hote = cible.get("nom", ""), cible.get("hote", "")
        port, utilisateur = cible.get("port", 22), cible.get("utilisateur", "")
        python, dossier = cible.get("python", ""), cible.get("dossier_tp", "")
        if not isinstance(nom, str) or not re.fullmatch(r"[a-z][a-z0-9_-]*", nom):
            raise ValueError("Utiliser un alias de cible simple : lettres, chiffres, - ou _.")
        if not isinstance(hote, str) or not re.fullmatch(r"[A-Za-z0-9_.:%-]+", hote):
            raise ValueError(f"Adresse incorrecte pour {nom}.")
        if type(port) is not int or not 1 <= port <= 65535:
            raise ValueError(f"Port incorrect pour {nom}.")
        if not isinstance(utilisateur, str) or not re.fullmatch(r"[a-z_][a-z0-9_-]*", utilisateur):
            raise ValueError(f"Utilisateur incorrect pour {nom}.")
        if not isinstance(python, str) or not PurePosixPath(python).is_absolute():
            raise ValueError(f"Indiquer le chemin Python absolu de {nom}.")
        if not isinstance(dossier, str):
            raise ValueError(f"Dossier incorrect pour {nom}.")
        chemin_tp = PurePosixPath(dossier)
        if not chemin_tp.is_absolute() or chemin_tp.name != "pyx-tp06" or ".." in chemin_tp.parts:
            raise ValueError(f"Le dossier dédié de {nom} doit être un chemin absolu vers pyx-tp06.")
        if nom in noms or (hote, port) in adresses:
            raise ValueError("Deux alias du même point d'accès ne constituent pas deux cibles.")
        noms.add(nom)
        adresses.add((hote, port))
        cible["port"] = port
    for champ in ["cle", "known_hosts"]:
        valeur = inventaire.get(champ)
        if not isinstance(valeur, str) or not valeur:
            raise ValueError(f"Champ manquant dans l'inventaire : {champ}.")
        fichier = Path(valeur).expanduser()
        if not fichier.is_absolute():
            fichier = chemin.parent / fichier
        if not fichier.is_file():
            raise ValueError(f"Fichier {champ} absent : vérifier la préparation SSH.")
        inventaire[champ] = str(fichier.resolve())
    return inventaire


def connexion(cible, inventaire):
    """Ne jamais accepter automatiquement une clé d'hôte inconnue."""
    client = Connection(
        cible["hote"],
        user=cible["utilisateur"],
        port=cible["port"],
        connect_timeout=3,
        connect_kwargs={
            "key_filename": inventaire["cle"],
            "allow_agent": False,
            "look_for_keys": False,
        },
    )
    ssh = client.client
    if ssh is None:
        raise RuntimeError("Le client SSH de Fabric n’est pas initialisé.")
    ssh.load_host_keys(inventaire["known_hosts"])
    ssh.set_missing_host_key_policy(RejectPolicy())
    return client


def collecter_une(cible, inventaire):
    """Collecter une cible ou lever une erreur : le client décide de la suite du parcours."""
    with connexion(cible, inventaire) as client:
        hostname = client.run("hostname", hide=True, timeout=3, in_stream=False).stdout.strip()
        systeme = client.run("uname -s", hide=True, timeout=3, in_stream=False).stdout.strip()
        disque = client.run(
            "LC_ALL=C df -Pk /", hide=True, timeout=3, in_stream=False
        ).stdout.splitlines()
        pourcentage = int(disque[-1].split()[4].rstrip("%"))
        if not hostname or systeme != "Linux" or not 0 <= pourcentage <= 100:
            raise ValueError("Identité ou mesure invalide.")
        return {
            "cible": cible["nom"],
            "date_utc": datetime.now(timezone.utc).isoformat(),
            "hostname": hostname,
            "systeme": systeme,
            "disque_utilise_pct": pourcentage,
            "statut": "ok",
            "erreur": "",
        }


def collecter(cibles=None, inventaire=None):
    inventaire = inventaire or charger_inventaire()
    resultats = []
    for cible in inventaire["cibles"] if cibles is None else cibles:
        try:
            mesure = collecter_une(cible, inventaire)
        except (
            OSError,
            SSHException,
            UnexpectedExit,
            CommandTimedOut,
            TimeoutError,
            ValueError,
            IndexError,
        ) as erreur:
            mesure = {
                "cible": cible["nom"],
                "date_utc": datetime.now(timezone.utc).isoformat(),
                "hostname": "",
                "systeme": "",
                "disque_utilise_pct": None,
                "statut": "erreur",
                "erreur": type(erreur).__name__,
            }
        resultats.append(mesure)
    return resultats
