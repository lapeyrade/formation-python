"""TP02 — Fiabiliser un import et réutiliser son code. Voir README.md dans ce dossier.

Un seul script et un seul bilan. Les blocs guidés préparent la production principale.
"""

import json
from pathlib import Path

from admin_tools.atelier import dossier_tp, preparer_etape, terminer
from admin_tools.chemins import DONNEES
from admin_tools.metier import lire_inventaire
from admin_tools.pilotes import projet_uv

dossier_tp_racine = dossier_tp("tp02")
resultats_tp = {}

# === FONCTIONS — Fonctions réutilisables (20 min) ===
dossier = preparer_etape(dossier_tp_racine, "fonctions")
resultat = None


def extraire_site(nom):
    return nom.split("-")[1]


# Cette étape suppose un entier entre 0 et 32, comme indiqué dans l’énoncé.
# return rend la valeur réutilisable ; print ne ferait que l’afficher.
def masque(prefixe):
    bits = "1" * prefixe + "0" * (32 - prefixe)
    octets = []
    for debut in range(0, 32, 8):
        octets.append(str(int(bits[debut : debut + 8], 2)))
    return ".".join(octets)


resultat = {
    "sites": [extraire_site("srv-paris-web-01"), extraire_site("srv-lyon-db-02")],
    "masques": [masque(24), masque(32)],
}

resultats_tp["fonctions"] = resultat

# === MUTABILITE — Mutabilité et effets de bord (10 min) ===
dossier = preparer_etape(dossier_tp_racine, "mutabilite")
resultat = None

original = ["ssh"]
# Une nouvelle liste suffit ici, car ses éléments sont des chaînes immuables.
# Avec des listes imbriquées, leurs objets resteraient partagés.
copie = original.copy()
copie.append("https")


def ajouter(element, elements=None):
    # Créer la liste à chaque appel évite de partager un paramètre par défaut mutable.
    # Tester None préserve aussi une liste vide explicitement fournie par l’appelant.
    if elements is None:
        elements = []
    elements.append(element)
    return elements


resultat = {"original": original, "copie": copie, "premier": ajouter("a"), "second": ajouter("b")}

resultats_tp["mutabilite"] = resultat

# === FICHIERS — Fichiers et exceptions (20 min) ===
dossier = preparer_etape(dossier_tp_racine, "fichiers")
resultat = None

# with ferme le fichier même si une opération échoue ; UTF-8 conserve les accents.
with (DONNEES / "message.txt").open(encoding="utf-8") as fichier:
    texte = fichier.read()
with (dossier / "copie.txt").open("w", encoding="utf-8") as fichier:
    fichier.write(texte)
# En binaire, aucun décodage : on doit retrouver exactement les mêmes octets.
with (DONNEES / "exemple.bin").open("rb") as fichier:
    octets = fichier.read()
with (dossier / "copie.bin").open("wb") as fichier:
    fichier.write(octets)
erreurs = []
try:
    (dossier / "source_absente.txt").read_text()
# Intercepter ce cas prévu laisse les autres erreurs visibles.
except FileNotFoundError:
    erreurs.append("fichier absent")
try:
    int("abc")
except ValueError:
    erreurs.append("conversion impossible")
# finally appartient à ce second try : il passe même après la conversion invalide.
finally:
    passage_finally = True
resultat = {
    "accent": "sécurité" in texte,
    "octets": len(octets),
    "copie_identique": (dossier / "copie.bin").read_bytes() == octets,
    "erreurs": erreurs,
    "finally": passage_finally,
}

resultats_tp["fichiers"] = resultat

# === INVENTAIRE — Inventaire fiable (35 min) ===
dossier = preparer_etape(dossier_tp_racine, "inventaire")
resultat = None

# Implémentation complète réutilisable : src/admin_tools/metier.py, lire_inventaire.
machines, rejets = lire_inventaire(DONNEES / "parc_source.csv")
(dossier / "rapport.txt").write_text("\n".join(m["nom"] for m in machines), encoding="utf-8")
(dossier / "rejets.json").write_text(
    json.dumps(rejets, ensure_ascii=False, indent=2), encoding="utf-8"
)
try:
    lire_inventaire(dossier / "absent.txt")
# Intercepter ce cas prévu laisse les autres erreurs visibles.
except FileNotFoundError:
    absence_signalee = True
resultat = {
    "acceptes": len(machines),
    "rejetes": len(rejets),
    "lignes_rejetees": [r["ligne"] for r in rejets],
    "absence_signalee": absence_signalee,
}

resultats_tp["inventaire"] = resultat

# === UV — Modules et projet uv (15 min) ===
dossier = preparer_etape(dossier_tp_racine, "uv")
resultat = None

# La solution séparée est importée sans lancer son bloc __main__.
# Le pilote prépare un projet uv neuf ; votre module de départ reste intact.
resultat = projet_uv(Path(__file__).parent / "solution" / "inventaire_module.py", dossier)

resultats_tp["uv"] = resultat

terminer(resultats_tp, dossier_tp_racine, principal="inventaire")
