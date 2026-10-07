"""Correction lisible : collecte et erreurs par cible, connexion fournie."""

from datetime import datetime, timezone

from invoke.exceptions import CommandTimedOut, UnexpectedExit
from paramiko import SSHException

from admin_tools.distant import connexion


def collecter_une(cible, inventaire):
    with connexion(cible, inventaire) as client:
        nom = client.run("hostname", hide=True, timeout=3, in_stream=False).stdout.strip()
        os = client.run("uname -s", hide=True, timeout=3, in_stream=False).stdout.strip()
        sortie = client.run("LC_ALL=C df -Pk /", hide=True, timeout=3, in_stream=False).stdout
        # LC_ALL=C fixe le format ; df -Pk fournit le pourcentage en cinquième colonne.
        pct = int(sortie.splitlines()[-1].split()[4].rstrip("%"))
        if not nom or os != "Linux" or not 0 <= pct <= 100:
            raise ValueError("Identité ou mesure invalide.")
        return {
            "cible": cible["nom"],
            "date_utc": datetime.now(timezone.utc).isoformat(),
            "hostname": nom,
            "systeme": os,
            "disque_utilise_pct": pct,
            "statut": "ok",
            "erreur": "",
        }


def collecter_parc(cibles, inventaire):
    lignes = []
    # Une erreur ne supprime pas les autres observations ; conserver aussi la cible en échec.
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
