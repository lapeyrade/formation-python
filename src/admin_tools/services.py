"""HTTP pédagogique, géolocalisation publique explicite, archives et SMTP local."""

import ipaddress
import smtplib
import tarfile
import zipfile
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path

import requests


def geolocaliser_publique(ip, timeout=3):
    """Un appel HTTPS explicite ; une estimation d'accès réseau, jamais de personne."""
    adresse = ipaddress.ip_address(ip)
    if not adresse.is_global:
        raise ValueError("Une adresse IP publique est attendue, hors réseaux d'exercice.")
    resultat = {
        "ip": str(adresse),
        "pays": None,
        "ville": None,
        "statut": "erreur",
        "source": "ipwho.is",
        "date_utc": datetime.now(timezone.utc).isoformat(),
    }
    try:
        reponse = requests.get(
            f"https://ipwho.is/{adresse}",
            params={"fields": "ip,success,country,city,message"},
            timeout=timeout,
        )
        reponse.raise_for_status()
        contenu = reponse.json()
        if not isinstance(contenu, dict) or contenu.get("ip") != str(adresse):
            return resultat
        if contenu.get("success") is False:
            resultat["statut"] = "indisponible"
        elif (
            contenu.get("success") is True
            and isinstance(contenu.get("country"), str)
            and contenu["country"].strip()
        ):
            ville = contenu.get("city")
            if ville is not None and not isinstance(ville, str):
                return resultat
            resultat.update(pays=contenu["country"], ville=ville, statut="localisee")
    except (requests.RequestException, ValueError):
        pass
    return resultat


def geolocaliser(ip, url, source="simulation_locale", timeout=3):
    ipaddress.ip_address(ip)
    resultat = {"ip": ip, "pays": None, "ville": None, "statut": "erreur", "source": source}
    try:
        reponse = requests.get(url, params={"ip": ip}, timeout=timeout)
        # Un corps JSON lisible ne garantit pas le succès HTTP : vérifier le statut d’abord.
        reponse.raise_for_status()
        contenu = reponse.json()
        if not isinstance(contenu, dict):
            return resultat
        if contenu.get("status") == "fail":
            resultat["statut"] = "indisponible"
        elif contenu.get("status") == "success" and contenu.get("country"):
            resultat.update(pays=contenu["country"], ville=contenu.get("city"), statut="localisee")
    # On traite les erreurs réseau/HTTP et de décodage ; le statut erreur reste explicite.
    except (requests.RequestException, ValueError):
        pass  # Le statut 'erreur' est une valeur explicite retournée à l'appelant.
    return resultat


def archiver(fichiers, destination):
    fichiers = [Path(p) for p in fichiers]
    destination = Path(destination)
    if len({p.name for p in fichiers}) != len(fichiers):
        raise ValueError("Les noms de fichiers doivent être uniques dans l'archive.")
    if any(not p.is_file() for p in fichiers):
        raise FileNotFoundError("Un fichier d'entrée manque.")
    if destination.resolve() in {p.resolve() for p in fichiers}:
        raise ValueError("L'archive ne peut pas contenir sa propre sortie.")
    if destination.suffix == ".zip":
        with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for fichier in fichiers:
                # Un nom simple rend l’archive indépendante des chemins du poste.
                archive.write(fichier, arcname=fichier.name)
    elif destination.name.endswith(".tar.gz"):
        with tarfile.open(destination, "w:gz") as archive:
            for fichier in fichiers:
                archive.add(fichier, arcname=fichier.name)
    else:
        raise ValueError("Format attendu : .zip ou .tar.gz")
    return destination


def envoyer_archive(archive, port, sujet="Rapport PYX", hote="127.0.0.1"):
    # Le kit est volontairement limité au SMTP local de capture.
    if hote != "127.0.0.1":
        raise ValueError("Utiliser le SMTP local de capture du kit.")
    message = EmailMessage()
    message["From"] = "formateur@example.test"
    message["To"] = "apprenant@example.test"
    message["Subject"] = sujet
    message.set_content("Rapport fictif de formation en pièce jointe.")
    archive = Path(archive)
    # read_bytes conserve le ZIP intact ; son type MIME décrit une archive binaire.
    message.add_attachment(
        archive.read_bytes(), maintype="application", subtype="zip", filename=archive.name
    )
    with smtplib.SMTP(hote, port, timeout=5) as smtp:
        smtp.send_message(message)
    return message
