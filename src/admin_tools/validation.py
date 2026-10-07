"""Contrôles des productions : ne pas se fier uniquement au bilan affiché."""

import hashlib
import json
import re
import sqlite3
import tarfile
import zipfile
from email import policy
from email.parser import BytesParser

import pandas as pd

from admin_tools.chemins import DONNEES
from admin_tools.configuration import contenu_configuration, valider_parametres
from admin_tools.systeme import lire_collecte


def verifier_productions(identifiant, dossier):
    attendus = {
        "diagnostic": ["diagnostic.json", "diagnostic.txt", "interpretation.json", "execution.log"],
        "bibliotheque": ["generer.txt", "resumer.txt"],
        "fichiers": ["copie.txt", "copie.bin"],
        "inventaire": ["rapport.txt", "rejets.json"],
        "uv": ["projet_uv/pyproject.toml", "projet_uv/uv.lock"],
        "arguments": ["compteurs.json", "alertes.json"],
        "pandas": ["nettoye.xlsx"],
        "rapport": ["rapport_complet.csv", "rapport_complet.xlsx", "alertes.csv", "alertes.xlsx"],
        "sqlite": ["incidents.sqlite"],
        "scrapy": ["machines.json"],
        "archives": ["rapport.zip", "rapport.tar.gz"],
        "email": ["rapport.zip", "message.eml"],
        "distant": [
            "execution.log",
            "ansible-apercu.txt",
            "ansible-preparation.txt",
            "ansible-premier.txt",
            "ansible-second.txt",
            "collecte.csv",
            "collecte-partielle.json",
            "preuve-ansible.json",
            "auth-collecte.log",
            "preuve-logs.json",
            "preuve-scripts.json",
            "ansible-scripts.txt",
        ],
        "integration": [
            "execution.log",
            "incidents.sqlite",
            "alertes.csv",
            "alertes.xlsx",
            "rapport.zip",
            "message.eml",
            "diagnostic.json",
        ],
    }
    for nom in attendus.get(identifiant, []):
        if not (dossier / nom).is_file():
            raise ValueError(f"Production manquante : {nom}")
    if identifiant in {"diagnostic", "distant", "integration"}:
        texte = (dossier / "execution.log").read_text(encoding="utf-8")
        evenements = re.findall(
            r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z (INFO|ERROR) etape=(\S+) cible=(\S+) .+",
            texte,
            re.M,
        )
        requis = {
            "diagnostic": {"diagnostic", "commande"},
            "distant": {"collecte", "echec_partiel", "ansible", "logs"},
            "integration": {"import", "archive", "smtp"},
        }[identifiant]
        if not requis <= {etape for _, etape, _ in evenements}:
            raise ValueError("Journal incomplet : dates, niveaux, étapes et cibles attendus.")
        if identifiant != "integration" and "ERROR" not in {niveau for niveau, _, _ in evenements}:
            raise ValueError("L'échec contrôlé doit être visible dans le journal.")
    if identifiant == "diagnostic":
        rapport = json.loads((dossier / "diagnostic.json").read_text())
        if not rapport["hostname"] or not rapport["systeme"]:
            raise ValueError("Identité absente du diagnostic")
        if (
            not rapport.get("utilisateur")
            or not rapport.get("date_utc")
            or not rapport.get("chemin_mesure")
        ):
            raise ValueError("Contexte absent du diagnostic")
        if (
            not 0 <= rapport["disque_libre"] <= rapport["disque_total"]
            or rapport["disque_total"] <= 0
        ):
            raise ValueError("Mesure disque incohérente")
        if rapport["execution"]["statut"] != "ok" or rapport["execution"]["code"] != 0:
            raise ValueError("La collecte de référence doit réussir")
        if rapport["hostname"] not in (dossier / "diagnostic.txt").read_text():
            raise ValueError("Le rapport lisible ne correspond pas au JSON")
        interpretations = json.loads((dossier / "interpretation.json").read_text())
        if set(interpretations) != {"memoire", "reseau", "services"}:
            raise ValueError("Trois observations Linux à interpréter.")
        for nom, interpretation in interpretations.items():
            if interpretation.get("observation") != rapport["observations_linux"][nom]:
                raise ValueError("L'interprétation ne décrit pas cet essai.")
            if not all(
                isinstance(interpretation.get(k), str) and interpretation[k].strip()
                for k in ("conclusion", "action")
            ):
                raise ValueError("Conclusion et prochaine action manquantes.")
    if identifiant == "bibliotheque":
        ips = [f"192.0.2.{i}" for i in range(1, 7)]
        resumes = [f"h{i} | 192.0.2.{i} | actif" for i in range(1, 7)]
        if (dossier / "generer.txt").read_text().splitlines() != ips:
            raise ValueError("Le client générateur doit produire les six IP du réseau.")
        if (dossier / "resumer.txt").read_text().splitlines() != resumes:
            raise ValueError("Le client résumé doit utiliser les six machines du package.")
    if identifiant == "fichiers":
        for original, copie in [("message.txt", "copie.txt"), ("exemple.bin", "copie.bin")]:
            if (DONNEES / original).read_bytes() != (dossier / copie).read_bytes():
                raise ValueError(f"Copie différente : {copie}")
    if identifiant == "inventaire":
        if len((dossier / "rapport.txt").read_text().splitlines()) != 8:
            raise ValueError("Le rapport doit contenir huit machines.")
        rejets = json.loads((dossier / "rejets.json").read_text())
        if [r["ligne"] for r in rejets] != [10, 11]:
            raise ValueError("Les lignes 10 et 11 doivent être rejetées.")
    if identifiant == "pandas":
        table = pd.read_excel(dossier / "nettoye.xlsx")
        if len(table) != 8 or (table["site"] == "inconnu").sum() != 1:
            raise ValueError("Le XLSX nettoyé doit contenir huit lignes et un site inconnu.")
    if identifiant in {"rapport", "integration"}:
        noms = ["rapport_complet", "alertes"] if identifiant == "rapport" else ["alertes"]
        for nom in noms:
            csv, xlsx = pd.read_csv(dossier / f"{nom}.csv"), pd.read_excel(dossier / f"{nom}.xlsx")
            pd.testing.assert_frame_equal(csv, xlsx)
            lignes, total = (3, 6) if nom == "rapport_complet" else (2, 5)
            if len(csv) != lignes or csv["echecs"].sum() != total:
                raise ValueError(f"Totaux incorrects dans {nom}.")
    if identifiant in {"sqlite", "integration"}:
        connexion = sqlite3.connect(
            (dossier / "incidents.sqlite").resolve().as_uri() + "?mode=ro", uri=True
        )
        try:
            if connexion.execute("SELECT count(*), sum(echecs) FROM incidents").fetchone() != (
                3,
                6,
            ):
                raise ValueError("Totaux incorrects dans SQLite.")
        finally:
            connexion.close()
    if identifiant == "scrapy":
        lignes = json.loads((dossier / "machines.json").read_text())
        if len(lignes) != 3 or [r.get("site") for r in lignes] != ["paris"] * 3:
            raise ValueError("L'export du spider doit contenir les trois sites.")
        if [r.get("etat") for r in lignes] != ["OK", "DEGRADE", "INCONNU"]:
            raise ValueError("États des services incorrects")
        if lignes[-1].get("message") != "non renseigné":
            raise ValueError("Message absent non traité")
    if identifiant in {"archives", "integration"}:
        noms = (
            ["rapport_complet.csv", "rapport_complet.xlsx"]
            if identifiant == "archives"
            else ["alertes.csv", "alertes.xlsx", "diagnostic.json"]
        )
        if identifiant == "integration":
            diagnostic = json.loads((dossier / "diagnostic.json").read_text())
            if not diagnostic.get("hostname") or not diagnostic.get("date_utc"):
                raise ValueError("Le diagnostic local doit décrire cet essai.")
            contexte = diagnostic["collecte_distante"]
            if contexte["statut"] == "complete":
                collecte = lire_collecte(dossier / "collecte.csv")
                if contexte["cibles"] != collecte:
                    raise ValueError("Le diagnostic ne correspond pas à la collecte jointe.")
                noms.append("collecte.csv")
            elif (
                contexte != {"statut": "non_executee", "cibles": []}
                or (dossier / "collecte.csv").exists()
            ):
                raise ValueError("La portée de la collecte distante est incohérente.")
        source = DONNEES if identifiant == "archives" else dossier
        with zipfile.ZipFile(dossier / "rapport.zip") as archive:
            if archive.namelist() != noms:
                raise ValueError("Liste des membres ZIP incorrecte.")
            for nom in noms:
                if archive.read(nom) != (source / nom).read_bytes():
                    raise ValueError(f"Le ZIP contient une version différente de {nom}.")
        if identifiant == "archives":
            with tarfile.open(dossier / "rapport.tar.gz") as archive:
                if archive.getnames() != noms:
                    raise ValueError("Liste des membres TAR incorrecte.")
                for nom in noms:
                    fichier = archive.extractfile(nom)
                    if fichier is None:
                        raise ValueError(f"Membre TAR non lisible : {nom}.")
                    with fichier:
                        if fichier.read() != (source / nom).read_bytes():
                            raise ValueError("Contenu TAR différent de la source.")
    if identifiant in {"email", "integration"}:
        message = BytesParser(policy=policy.default).parsebytes(
            (dossier / "message.eml").read_bytes()
        )
        pieces = list(message.iter_attachments())
        if (
            len(pieces) != 1
            or pieces[0].get_payload(decode=True) != (dossier / "rapport.zip").read_bytes()
        ):
            raise ValueError("Pièce jointe absente ou différente du ZIP.")
    if identifiant == "distant":
        from admin_tools.distant import charger_inventaire

        noms = [c["nom"] for c in charger_inventaire()["cibles"]]
        collecte = lire_collecte(dossier / "collecte.csv", noms)
        if [c["cible"] for c in collecte] != noms:
            raise ValueError("Collecte distante incomplète")
        scripts = json.loads((dossier / "preuve-scripts.json").read_text())
        if [(s["cible"], s["hostname"], s["systeme"]) for s in scripts] != [
            (m["cible"], m["hostname"], m["systeme"]) for m in collecte
        ]:
            raise ValueError(
                "Le script doit avoir été exécuté sur les cibles configurées collectées."
            )
        from admin_tools.metier import analyser_logs

        logs = json.loads((dossier / "preuve-logs.json").read_text())
        if (
            logs["source"] != "logs_fictifs_distants"
            or [s["cible"] for s in logs["sources"]] != noms
        ):
            raise ValueError("La provenance des logs ne décrit pas les cibles configurées.")
        contenu = b""
        debut = 1
        for source in logs["sources"]:
            if source["fichier"] != f"{source['cible']}.log":
                raise ValueError("Nom de log incohérent.")
            octets = (dossier / "logs" / source["fichier"]).read_bytes()
            lignes = octets.splitlines(keepends=True)
            if (
                source["sha256"],
                source["octets"],
                source["lignes"],
                source["debut"],
                source["fin"],
            ) != (
                hashlib.sha256(octets).hexdigest(),
                len(octets),
                len(lignes),
                debut,
                debut + len(lignes) - 1,
            ):
                raise ValueError("Le manifeste ne correspond pas aux logs reçus.")
            contenu += b"".join(
                ligne if ligne.endswith(b"\n") else ligne + b"\n" for ligne in lignes
            )
            debut += len(lignes)
        if (dossier / "auth-collecte.log").read_bytes() != contenu:
            raise ValueError(
                "Le regroupement doit conserver toutes les lignes des cibles configurées."
            )
        analyse = analyser_logs(dossier / "auth-collecte.log")
        if logs["analyse"] != analyse or analyse != {
            "compteurs": {"192.0.2.42": len(noms)},
            "rejets": [],
            "valides": 2 * len(noms),
            "succes": len(noms),
        }:
            raise ValueError("L'analyse des logs distants est incorrecte.")
        partiel = json.loads((dossier / "collecte-partielle.json").read_text())
        if [m["statut"] for m in partiel] != ["ok", "erreur"]:
            raise ValueError("Échec partiel non visible")
        preuve = json.loads((dossier / "preuve-ansible.json").read_text())
        if preuve["cibles"] != noms or [f["cible"] for f in preuve["fichiers"]] != noms:
            raise ValueError("La preuve Ansible ne décrit pas les cibles demandées.")
        parametres = valider_parametres(preuve["parametres"])
        if preuve["avant_apercu"] != preuve["apres_apercu"]:
            raise ValueError("L'aperçu ne doit pas modifier la configuration.")
        if set(preuve["apercu"]) != set(noms) or any(
            r["failed"] or r["unreachable"] for r in preuve["apercu"].values()
        ):
            raise ValueError("Aperçu incomplet ou en échec.")
        for passage in ["premier", "second"]:
            recap = preuve[passage]
            if set(recap) != set(noms) or any(
                r["ok"] < 2 or r["failed"] or r["unreachable"] for r in recap.values()
            ):
                raise ValueError("Un passage Ansible n'a pas réussi sur toutes les cibles.")
        if any(r["changed"] != 0 for r in preuve["second"].values()):
            raise ValueError("Le second passage Ansible doit conserver l'état souhaité.")
        for fichier in preuve["fichiers"]:
            if (
                fichier["contenu"] != contenu_configuration(fichier["cible"], parametres)
                or fichier["mode"] != "0640"
            ):
                raise ValueError(
                    "Le fichier distant ne correspond pas au contenu et au mode attendus."
                )


def attendus_pour_etape(etape):
    """Adapter les volumes de preuve au nombre de cibles, sans changer les critères métier."""
    attendus = dict(etape["attendus"])
    if etape["cle"] == "distant":
        from admin_tools.distant import charger_inventaire

        nombre = len(charger_inventaire()["cibles"])
        attendus.update(
            logs_telecharges=nombre,
            evenements_logs=2 * nombre,
            echecs_logs=nombre,
            scripts_executes=nombre,
        )
    return attendus
