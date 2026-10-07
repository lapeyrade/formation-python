"""Qualifier le parc : compléter les repères TODO, puis exécuter un bloc à la fois."""

# SEUL FICHIER À MODIFIER : cinq TODO dans les blocs TYPES, BOUCLES et MASQUES.
# Conserver les imports, les repères # ===, les données et les calculs fournis.
# Après chaque modification : enregistrer puis lancer le contrôle de l'étape.

from ipaddress import ip_network

from admin_tools.atelier import dossier_tp, preparer_etape, terminer
from parc import PARC, MachineNormalisee

# Fourni : chaque lancement crée un nouvel essai, sans écraser les précédents.
dossier_tp_racine = dossier_tp("tp01")
resultats_tp = {}

# === TYPES — Normaliser les données du parc (25 min) ===
# À FAIRE : une modification, sur la valeur du champ "actif" ci-dessous.
# Comparer ligne["actif"] à "oui" avec == ; garder la virgule finale.
# Le nettoyage des noms, les ports, les sites et les compteurs sont déjà fournis.
# Contrôle : uv run python outils/verifier.py tp01 --etape types
dossier = preparer_etape(dossier_tp_racine, "types")
machines: list[MachineNormalisee] = []
for ligne in PARC:
    nom = ligne["nom"].strip().lower()
    # **ligne construit une nouvelle ligne : la source PARC reste intacte.
    machines.append(
        {
            **ligne,
            "nom": nom,
            "site": nom.split("-")[1],
            "port": int(ligne["port"]),
            "actif": False,  # TODO 1 : comparer explicitement le champ reçu à "oui".
        }
    )
# Fourni : les sorties sont calculées, jamais recopiées depuis les valeurs attendues.
resultat = {
    "machines": len(machines),
    "premier": machines[0]["nom"],
    "port_entier": machines[0]["port"],
    "sites": sorted({m["site"] for m in machines}),
    "actives": sum(m["actif"] for m in machines),
}
resultats_tp["types"] = resultat

# === BOUCLES — Prioriser les contrôles (20 min) ===
# À FAIRE : remplacer False dans le if, puis ajouter une ligne dans le while.
# Les compteurs et le bilan sont fournis. Ne pas réécrire le bloc entier.
# Contrôle : uv run python outils/verifier.py tp01 --etape boucles
dossier = preparer_etape(dossier_tp_racine, "boucles")
# On repart de PARC : ce bloc ne dépend pas du résultat du bloc TYPES.
prioritaires = []
for ligne in PARC:
    # TODO 1 : remplacer False par ligne["actif"] == "oui" and ligne["charge"] >= 80.
    if False:
        prioritaires.append(ligne["nom"].strip().lower())
inactives = sum(ligne["actif"] == "non" for ligne in PARC)
tentatives = []
for reponses in [[False, True], [False, False, False]]:
    essais, succes = 0, False
    while essais < 3 and not succes:
        # TODO 2 : ajouter succes = reponses[essais] AVANT essais += 1.
        # Même indentation que la ligne suivante ; lire l'indice 0 au premier tour.
        essais += 1  # Fourni : la borne assure la fin même sans succès.
    tentatives.append(essais)
resultat = {"prioritaires": prioritaires, "inactives": inactives, "tentatives": tentatives}
resultats_tp["boucles"] = resultat

# === MASQUES — Préparer le plan réseau (40 min) ===
# À FAIRE : remplacer pass par un append, puis None par une liste filtrée.
# Le masque assemblé, les capacités et les compteurs par site sont déjà fournis.
# Contrôle : uv run python outils/verifier.py tp01 --etape masques
dossier = preparer_etape(dossier_tp_racine, "masques")
masques, capacites = [], []
for prefixe in [24, 27, 29]:
    bits = "1" * prefixe + "0" * (32 - prefixe)
    octets = []
    for debut in range(0, 32, 8):
        # TODO 1 : remplacer pass par octets.append(str(int(bits[debut : debut + 8], 2))).
        # Lecture de 8 caractères -> entier binaire -> texte -> ajout à la liste.
        pass
    masque = ".".join(octets)
    reseau = ip_network(f"192.0.2.0/{prefixe}")
    # Observer le masque de référence, puis comparer au calcul une fois complété.
    print("Préfixe", prefixe, "référence", reseau.netmask, "calcul", masque)
    masques.append(masque)
    # Cette capacité n'est valable ici que pour /24, /27 et /29, pas /31 ou /32.
    capacites.append(reseau.num_addresses - 2)
resultat = {
    "masques": masques,
    "capacites": capacites,
    # TODO 2 : remplacer None par [p for p in [-1, 24, 33] if p < 0 or p > 32].
    # Lister les valeurs invalides ; pas d'exception à lever dans cet exercice.
    "prefixes_invalides": None,
    "sites": {
        site: sum(site == m["nom"].strip().lower().split("-")[1] for m in PARC)
        for site in ["lyon", "paris"]
    },
}
resultats_tp["masques"] = resultat

terminer(resultats_tp, dossier_tp_racine, principal="masques")
