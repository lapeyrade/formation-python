"""Fiabiliser l'import : compléter les TODO ; lectures et sorties sont guidées."""

import csv
import ipaddress
import json
from pathlib import Path

from admin_tools.atelier import dossier_tp, preparer_etape, terminer
from admin_tools.chemins import DONNEES
from admin_tools.pilotes import projet_uv

dossier_tp_racine = dossier_tp("tp02")
resultats_tp = {}

# === FONCTIONS — Fonctions réutilisables (20 min) ===
# CONSIGNE : Deux retours de fonctions.
# FICHIER : depart.py. Voir README.md, section fonctions.
dossier = preparer_etape(dossier_tp_racine, "fonctions")


def extraire_site(nom):
    morceaux = nom.split("-")
    print("Segments à examiner :", morceaux)
    # TODO 1 : renvoyer le segment du site ; enlever le print après l'observation.
    return None


def masque(prefixe):
    # Fourni : calcul repris du TP01 ; on travaille ici la valeur de retour.
    bits = "1" * prefixe + "0" * (32 - prefixe)
    octets = [str(int(bits[debut : debut + 8], 2)) for debut in range(0, 32, 8)]
    print("Octets calculés :", octets)
    # TODO 2 : renvoyer les octets réunis par des points ; retirer ce print.
    return None


resultat = {
    "sites": [extraire_site("srv-paris-web-01"), extraire_site("srv-lyon-db-02")],
    "masques": [masque(24), masque(32)],
}
resultats_tp["fonctions"] = resultat

# === MUTABILITE — Mutabilité et effets de bord (10 min) ===
# CONSIGNE : Deux partages de liste à corriger.
# FICHIER : depart.py. Voir README.md, section mutabilite.
dossier = preparer_etape(dossier_tp_racine, "mutabilite")
original = ["ssh"]
copie = original  # TODO 1 : créer une copie indépendante avant l'ajout.
copie.append("https")


def ajouter(element, elements=[]):  # TODO 2 : None par défaut, liste neuve si None.
    elements.append(element)
    return elements


# Fourni : ces appels rendent visibles les deux effets de bord à corriger.
resultat = {"original": original, "copie": copie, "premier": ajouter("a"), "second": ajouter("b")}
resultats_tp["mutabilite"] = resultat

# === FICHIERS — Fichiers et exceptions (20 min) ===
# CONSIGNE : Une copie binaire et trois traitements d’erreur.
# FICHIER : depart.py et debogage.py. Voir README.md, section fichiers.
dossier = preparer_etape(dossier_tp_racine, "fichiers")
# Fourni : with ferme le fichier et UTF-8 conserve les accents.
with (DONNEES / "message.txt").open(encoding="utf-8") as fichier:
    texte = fichier.read()
with (dossier / "copie.txt").open("w", encoding="utf-8") as fichier:
    fichier.write(texte)
with (DONNEES / "exemple.bin").open("rb") as fichier:
    octets = fichier.read()
# TODO 1 : ouvrir dossier / "copie.bin" en "wb" et écrire octets.
erreurs = []
passage_finally = False
try:
    (dossier / "source_absente.txt").read_text()
except FileNotFoundError:
    # TODO 2 : conserver "fichier absent" dans erreurs.
    pass
try:
    int("abc")
except ValueError:
    # TODO 3 : conserver "conversion impossible" dans erreurs.
    pass
finally:
    # TODO 4 : marquer passage_finally ; ce bloc passe aussi après l'exception.
    pass
resultat = {
    "accent": "sécurité" in texte,
    "octets": len(octets),
    # Le garde permet de lancer le squelette avant d'avoir écrit la copie.
    "copie_identique": (dossier / "copie.bin").is_file()
    and (dossier / "copie.bin").read_bytes() == octets,
    "erreurs": erreurs,
    "finally": passage_finally,
}
resultats_tp["fichiers"] = resultat

# === INVENTAIRE — Inventaire fiable (35 min) ===
# CONSIGNE : Valider une ligne, puis traiter un fichier absent.
# FICHIER : depart.py. Voir README.md, section inventaire.
dossier = preparer_etape(dossier_tp_racine, "inventaire")


def valider_ligne(ligne):
    # Fourni : rejeter une ligne incomplète avant les conversions.
    if None in ligne or any(v is None for v in ligne.values()):
        raise ValueError("4 champs attendus")
    ipaddress.ip_address(ligne["ip"])
    if ligne["actif"] not in {"oui", "non"}:
        raise ValueError("actif doit être oui ou non")
    charge = int(ligne["charge"])
    # TODO 1 : rejeter une charge hors de 0 à 100 avec ValueError.
    print("Ligne à normaliser :", ligne["nom"], charge)
    # TODO 2 : renvoyer un dict nom/ip/actif/charge ; actif devient un booléen.
    # Enlever le print une fois le résultat construit.
    return None


def importer(source):
    machines, rejets = [], []
    # L'ouverture reste hors du try par ligne : un fichier absent arrête l'import.
    with source.open(encoding="utf-8-sig", newline="") as fichier:
        lecteur = csv.DictReader(fichier, delimiter=";")
        if lecteur.fieldnames != ["nom", "ip", "actif", "charge"]:
            raise ValueError("En-tête attendu : nom;ip;actif;charge")
        for ligne in lecteur:
            try:
                machine = valider_ligne(ligne)
                if machine is not None:  # Garde du squelette tant que le retour manque.
                    machines.append(machine)
            except ValueError as erreur:
                rejets.append({"ligne": lecteur.line_num, "motif": str(erreur), "source": ligne})
    return machines, rejets


machines, rejets = importer(DONNEES / "parc_source.csv")
(dossier / "rapport.txt").write_text("\n".join(m["nom"] for m in machines), encoding="utf-8")
(dossier / "rejets.json").write_text(
    json.dumps(rejets, ensure_ascii=False, indent=2), encoding="utf-8"
)
absence_signalee = None  # TODO 3 : tester importer(dossier / "absent.txt") dans try/except.
resultat = {
    "acceptes": len(machines),
    "rejetes": len(rejets),
    "lignes_rejetees": [r["ligne"] for r in rejets],
    "absence_signalee": absence_signalee,
}
resultats_tp["inventaire"] = resultat

# === UV — Modules et projet uv (15 min) ===
# CONSIGNE : Une valeur de retour et un projet d’essai.
# FICHIER : inventaire_module.py. Voir README.md, section uv.
dossier = preparer_etape(dossier_tp_racine, "uv")
# TODO : compléter etiquette dans inventaire_module.py ; le pilote gère l'installation.
resultat = projet_uv(Path(__file__).with_name("inventaire_module.py"), dossier)
resultats_tp["uv"] = resultat

terminer(resultats_tp, dossier_tp_racine, principal="inventaire")
