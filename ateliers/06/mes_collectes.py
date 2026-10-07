"""Collecte Fabric guidée : compléter la mesure disque ; boucle et erreurs fournies.

Une ligne par cible : cible, date_utc, hostname, systeme, disque_utilise_pct, statut, erreur.
Les cibles SSH sont préparées avant le TP ; leur connexion est fournie.
"""

from datetime import datetime, timezone

from invoke.exceptions import CommandTimedOut, UnexpectedExit
from paramiko import SSHException

# Aide du cours : configure Fabric et vérifie les clés SSH du laboratoire.
# connexion n’est pas une fonction standard de Python ni le nom de la classe Fabric.
from admin_tools.distant import connexion


def collecter_une(cible, inventaire):
    with connexion(cible, inventaire) as client:
        # hide évite une sortie mélangée ; timeout borne l'attente ; in_stream=False évite une saisie.
        nom = client.run("hostname", hide=True, timeout=3, in_stream=False).stdout.strip()
        systeme = client.run("uname -s", hide=True, timeout=3, in_stream=False).stdout.strip()
        sortie = client.run("LC_ALL=C df -Pk /", hide=True, timeout=3, in_stream=False).stdout
        print("df à interpréter pour", cible["nom"], "\n", sortie)
        # TODO : dernière ligne, cinquième colonne ; enlever % puis convertir avec int.
        # Exemple de découpage : sortie.splitlines()[-1].split()[4].rstrip("%")
        pct: int | None = None
        if pct is None:
            raise ValueError("TODO : compléter la mesure disque dans mes_collectes.py")
        if not nom or systeme != "Linux" or not 0 <= pct <= 100:
            raise ValueError("Identité ou mesure invalide.")
        return {
            "cible": cible["nom"],
            "date_utc": datetime.now(timezone.utc).isoformat(),
            "hostname": nom,
            "systeme": systeme,
            "disque_utilise_pct": pct,
            "statut": "ok",
            "erreur": "",
        }


def collecter_parc(cibles, inventaire):
    lignes = []
    for cible in cibles:
        try:
            ligne = collecter_une(cible, inventaire)
        except (
            OSError,
            SSHException,
            UnexpectedExit,
            CommandTimedOut,
            TimeoutError,
            ValueError,
            IndexError,
        ) as erreur:
            # L'erreur appartient à cette cible ; le prochain tour conserve les autres succès.
            # Aucun secret ni détail de connexion dans ce rapport.
            ligne = {
                "cible": cible["nom"],
                "date_utc": datetime.now(timezone.utc).isoformat(),
                "hostname": "",
                "systeme": "",
                "disque_utilise_pct": None,
                "statut": "erreur",
                "erreur": type(erreur).__name__,
            }
        lignes.append(ligne)
    return lignes
