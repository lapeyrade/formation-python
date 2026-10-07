"""Diagnostic local en lecture seule : contexte, disque et observations Linux."""

import csv
import getpass
import json
import platform
import shutil
import socket
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def lancer(commande, timeout=3):
    """Garder succès, échec, absence et délai dépassé distincts ; ne jamais interpréter une chaîne via un shell."""
    try:
        resultat = subprocess.run(
            commande, capture_output=True, text=True, errors="replace", timeout=timeout, check=False
        )
        return {
            "statut": "ok" if resultat.returncode == 0 else "echec",
            "code": resultat.returncode,
            "stdout": resultat.stdout.strip(),
            "stderr": resultat.stderr.strip(),
        }
    except FileNotFoundError as erreur:
        return {"statut": "absente", "code": None, "stdout": "", "stderr": str(erreur)}
    except subprocess.TimeoutExpired:
        return {"statut": "timeout", "code": None, "stdout": "", "stderr": "délai dépassé"}


def observer_linux(meminfo=Path("/proc/meminfo")):
    """Conserver les limites de mesure ; une source inaccessible n'est pas un résultat sain."""
    if platform.system() != "Linux":
        return {
            nom: {"statut": "non_applicable", "detail": "Observation Linux uniquement."}
            for nom in ("memoire", "reseau", "services")
        }
    try:
        valeurs = dict(ligne.split(":", 1) for ligne in Path(meminfo).read_text().splitlines())
        total = int(valeurs["MemTotal"].split()[0])
        disponible = int(valeurs["MemAvailable"].split()[0])
        if not 0 <= disponible <= total or total <= 0:
            raise ValueError("mesure incohérente")
        memoire = {
            "statut": "ok",
            "total_kio": total,
            "disponible_kio": disponible,
            "utilise_pct": round((total - disponible) / total * 100, 1),
            "detail": "Instantané de MemAvailable ; ne prouve pas une fuite mémoire.",
        }
    except OSError as erreur:
        memoire = {"statut": "inaccessible", "detail": type(erreur).__name__}
    except (ValueError, KeyError, IndexError) as erreur:
        memoire = {"statut": "invalide", "detail": type(erreur).__name__}
    interfaces = lancer(["ip", "-j", "address", "show"])
    routes = lancer(["ip", "-j", "route", "show"])
    reseau = {
        "statut": "ok",
        "interfaces": interfaces,
        "routes": routes,
        "detail": "Configuration locale ; une route ne prouve pas la connectivité.",
    }
    for resultat in (interfaces, routes):
        if resultat["statut"] != "ok":
            reseau["statut"] = resultat["statut"]
            break
        try:
            if not isinstance(json.loads(resultat["stdout"]), list):
                raise ValueError("liste JSON attendue")
        except (ValueError, TypeError):
            reseau["statut"] = "invalide"
            break
    execution = lancer(["systemctl", "--failed", "--no-legend", "--plain", "--no-pager"])
    services = {
        "statut": execution["statut"],
        "execution": execution,
        "nombre_echecs": len(execution["stdout"].splitlines())
        if execution["statut"] == "ok"
        else None,
        "detail": "Unités en échec connues de systemd ; ne prouve pas que tous les services répondent.",
    }
    return {"memoire": memoire, "reseau": reseau, "services": services}


def collecter_local(chemin):
    chemin = Path(chemin).resolve()
    systeme = platform.system()
    disque = shutil.disk_usage(chemin)
    commande = ["whoami"] if systeme == "Windows" else ["uname", "-s"]
    return {
        "observations_linux": observer_linux(),
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "utilisateur": getpass.getuser(),
        "hostname": socket.gethostname(),
        "systeme": systeme,
        "chemin_mesure": str(chemin),
        "disque_total": disque.total,
        "disque_libre": disque.free,
        "disque_utilise_pct": round(disque.used / disque.total * 100, 1),
        "commande": commande,
        "execution": lancer(commande),
        "commandes": {
            "identite": lancer(["whoami"] if systeme == "Windows" else ["id"]),
            "volume": lancer(["df", "-Pk", str(chemin)]) if systeme != "Windows" else None,
        },
    }


def enregistrer(rapport, dossier):
    dossier = Path(dossier)
    (dossier / "diagnostic.json").write_text(json.dumps(rapport, indent=2), encoding="utf-8")
    lignes = [
        f"Date UTC : {rapport['date_utc']}",
        f"Utilisateur : {rapport['utilisateur']}",
        f"Hôte : {rapport['hostname']}",
        f"OS : {rapport['systeme']}",
        f"Chemin mesuré : {rapport['chemin_mesure']}",
        f"Disque utilisé : {rapport['disque_utilise_pct']} %",
        f"Commande : {rapport['commande']}",
        f"État : {rapport['execution']['statut']}",
        f"Résultat : {rapport['execution']['stdout']}",
        f"Diagnostic : {rapport['execution']['stderr']}",
    ]
    for nom, resultat in rapport["commandes"].items():
        if resultat is not None:
            lignes.extend(
                [
                    f"Commande {nom} : {resultat['statut']} (code {resultat['code']})",
                    resultat["stdout"],
                    resultat["stderr"],
                ]
            )
    for nom, observation in rapport["observations_linux"].items():
        lignes.extend(
            [
                f"Observation {nom} : {observation['statut']}",
                json.dumps(observation, ensure_ascii=False),
            ]
        )
    (dossier / "diagnostic.txt").write_text("\n".join(lignes) + "\n", encoding="utf-8")


def lire_collecte(chemin, cibles_attendues=None):
    """Lire une collecte complète ; refuser la diffusion d'un rapport partiel."""
    with Path(chemin).open(newline="", encoding="utf-8") as fichier:
        lecteur = csv.DictReader(fichier)
        requis = {"cible", "hostname", "systeme", "date_utc", "disque_utilise_pct", "statut"}
        if not requis <= set(lecteur.fieldnames or []):
            raise ValueError("Colonnes de collecte manquantes.")
        lignes = list(lecteur)
    noms = [ligne["cible"] for ligne in lignes]
    if not lignes or len(set(noms)) != len(noms) or not all(noms):
        raise ValueError("La collecte doit identifier au moins une cible, sans doublon.")
    if cibles_attendues is not None and noms != list(cibles_attendues):
        raise ValueError("Collecte incomplète : les cibles ne correspondent pas à l’inventaire.")
    for ligne in lignes:
        if ligne["statut"] != "ok":
            raise ValueError(
                "Collecte partielle : conserver le diagnostic, sans diffuser le rapport final."
            )
        date = datetime.fromisoformat(ligne["date_utc"])
        if not ligne["hostname"] or ligne["systeme"] != "Linux" or date.utcoffset() is None:
            raise ValueError("Identité ou date absente de la collecte.")
        if not 0 <= float(ligne["disque_utilise_pct"]) <= 100:
            raise ValueError("Mesure disque incohérente dans la collecte.")
    return lignes


def joindre_diagnostic(dossier, collecte=None):
    """Préparer les pièces de diagnostic du même essai, sans joindre les clés SSH."""
    distant = lire_collecte(collecte) if collecte is not None else []
    dossier = Path(dossier)
    rapport = collecter_local(dossier)
    rapport["collecte_distante"] = {
        "statut": "complete" if distant else "non_executee",
        "cibles": distant,
    }
    enregistrer(rapport, dossier)
    fichiers = [dossier / "diagnostic.json"]
    if collecte is not None:
        destination = dossier / "collecte.csv"
        if Path(collecte).resolve() != destination.resolve():
            shutil.copyfile(collecte, destination)
        fichiers.append(destination)
    return fichiers
