"""Corrigés réutilisables : inventaire, IP, logs et arguments."""

import argparse
import csv
import ipaddress
import re
from pathlib import Path


class Machine:
    def __init__(self, nom, ip, actif=True):
        self.nom = nom
        self.ip = ip
        self.actif = actif

    def resume(self):
        return f"{self.nom} | {self.ip} | {'actif' if self.actif else 'inactif'}"


def masque_ipv4(prefixe):
    if type(prefixe) is not int or not 0 <= prefixe <= 32:
        raise ValueError("Le préfixe doit être un entier de 0 à 32.")
    bits = "1" * prefixe + "0" * (32 - prefixe)
    return ".".join(str(int(bits[i : i + 8], 2)) for i in range(0, 32, 8))


def generer_ips(reseau, reservees=(), limite=None):
    """Adresses candidates non réservées ; aucune sonde ne prouve leur disponibilité."""
    if limite is not None and (type(limite) is not int or limite < 0):
        raise ValueError("limite doit être un entier positif ou nul")
    net = ipaddress.ip_network(reseau)
    if net.version != 4:
        raise ValueError("Le plan de ce laboratoire est IPv4")
    reservees = {ipaddress.ip_address(ip) for ip in reservees}
    if any(ip not in net for ip in reservees):
        raise ValueError("Réservation hors du réseau")
    if limite == 0:
        return
    nombre = 0
    for adresse in net.hosts():
        if adresse in reservees:
            continue
        yield str(adresse)
        nombre += 1
        if limite is not None and nombre >= limite:
            return


def lire_inventaire(source):
    machines, rejets = [], []
    with Path(source).open(encoding="utf-8-sig", newline="") as fichier:
        lecteur = csv.DictReader(fichier, delimiter=";")
        if lecteur.fieldnames != ["nom", "ip", "actif", "charge"]:
            raise ValueError("En-tête attendu : nom;ip;actif;charge")
        for ligne in lecteur:
            try:
                if None in ligne or any(v is None for v in ligne.values()):
                    raise ValueError("4 champs attendus")
                nom, ip, actif = ligne["nom"], ligne["ip"], ligne["actif"]
                ipaddress.ip_address(ip)
                if actif not in {"oui", "non"}:
                    raise ValueError("actif doit être oui ou non")
                charge = int(ligne["charge"])
                if not 0 <= charge <= 100:
                    raise ValueError("charge hors de 0 à 100")
                machines.append({"nom": nom, "ip": ip, "actif": actif == "oui", "charge": charge})
            except ValueError as erreur:
                rejets.append({"ligne": lecteur.line_num, "motif": str(erreur), "source": ligne})
    return machines, rejets


# Échantillon syslog OpenSSH : mot de passe refusé, utilisateur inconnu ou clé acceptée.
MOTIF = re.compile(
    r"^[A-Z][a-z]{2}\s+\d{1,2} \d{2}:\d{2}:\d{2} \S+ sshd\[\d+\]: "
    r"(?P<statut>Failed password|Accepted publickey) for (?:invalid user )?"
    r"(?P<user>\S+) from (?P<ip>\S+) port \d+ ssh2$"
)


def analyser_logs(source):
    compteurs, rejets = {}, []
    valides = succes = 0
    # L’ouverture reste hors du try de chaque ligne : une source absente arrête l’import.
    with Path(source).open(encoding="utf-8") as fichier:
        for numero, ligne in enumerate(fichier, 1):
            texte = ligne.rstrip("\n")
            match = MOTIF.fullmatch(texte)
            if match is None:
                rejets.append({"ligne": numero, "motif": "format", "source": texte})
                continue
            ip = match["ip"]
            try:
                # La regex extrait le champ ; ipaddress rejette aussi les octets impossibles.
                ipaddress.ip_address(ip)
            except ValueError:
                rejets.append({"ligne": numero, "motif": "IP invalide", "source": texte})
                continue
            # Ne compter que les événements dont le format ET l’adresse ont été validés.
            valides += 1
            if match["statut"] == "Accepted publickey":
                succes += 1
            else:
                compteurs[ip] = compteurs.get(ip, 0) + 1
    return {"compteurs": compteurs, "rejets": rejets, "valides": valides, "succes": succes}


def positif(texte):
    try:
        valeur = int(texte)
    except ValueError as erreur:
        raise argparse.ArgumentTypeError("un entier positif est attendu") from erreur
    if valeur <= 0:
        raise argparse.ArgumentTypeError("le seuil doit être supérieur à zéro")
    return valeur


def parseur_logs():
    parseur = argparse.ArgumentParser(description="Analyser les échecs du log fictif.")
    parseur.add_argument("source", type=Path)
    parseur.add_argument("--seuil", type=positif, default=2)
    parseur.add_argument("--sortie", type=Path, default=Path("sorties/logs"))
    return parseur


MOTIF_WEB = re.compile(
    r'^\S+ - - \[[^]]+\] "[A-Z]+ (?P<url>\S+) HTTP/[0-9.]+" (?P<status>\d{3}) \d+$'
)


def analyser_web(source):
    """Compter les erreurs HTTP sans assimiler une 4xx à une intrusion."""
    compteurs = {"4xx": 0, "5xx": 0}
    rejets = 0
    with Path(source).open(encoding="utf-8") as fichier:
        for ligne in fichier:
            match = MOTIF_WEB.fullmatch(ligne.strip())
            if match is None:
                rejets += 1
                continue
            statut = int(match["status"])
            if 400 <= statut < 500:
                compteurs["4xx"] += 1
            elif 500 <= statut < 600:
                compteurs["5xx"] += 1
    return {**compteurs, "rejets": rejets}
