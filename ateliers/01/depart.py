"""Qualifier le parc : compléter les repères TODO, puis exécuter un bloc à la fois."""

from ipaddress import ip_network

from admin_tools.atelier import dossier_tp, preparer_etape, terminer
from parc import PARC, MachineNormalisee

# Fourni : chaque lancement crée un nouvel essai, sans écraser les précédents.
dossier_tp_racine = dossier_tp("tp01")
resultats_tp = {}

# === TYPES — Normaliser les données du parc (25 min) ===
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
dossier = preparer_etape(dossier_tp_racine, "boucles")
# On repart de PARC : ce bloc ne dépend pas du résultat du bloc TYPES.
prioritaires = []
for ligne in PARC:
    # TODO 1 : remplacer False par actif == "oui" ET charge >= 80.
    if False:
        prioritaires.append(ligne["nom"].strip().lower())
inactives = sum(ligne["actif"] == "non" for ligne in PARC)
tentatives = []
for reponses in [[False, True], [False, False, False]]:
    essais, succes = 0, False
    while essais < 3 and not succes:
        # TODO 2 : lire reponses[essais] dans succes AVANT d'incrémenter essais.
        essais += 1  # Fourni : la borne assure la fin même sans succès.
    tentatives.append(essais)
resultat = {"prioritaires": prioritaires, "inactives": inactives, "tentatives": tentatives}
resultats_tp["boucles"] = resultat

# === MASQUES — Préparer le plan réseau (40 min) ===
dossier = preparer_etape(dossier_tp_racine, "masques")
masques, capacites = [], []
for prefixe in [24, 27, 29]:
    bits = "1" * prefixe + "0" * (32 - prefixe)
    octets = []
    for debut in range(0, 32, 8):
        # TODO 1 : ajouter str(int(bits[debut : debut + 8], 2)) à octets.
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
    "prefixes_invalides": None,  # TODO 2 : filtrer [-1, 24, 33] hors de 0 <= p <= 32.
    "sites": {
        site: sum(site == m["nom"].strip().lower().split("-")[1] for m in PARC)
        for site in ["lyon", "paris"]
    },
}
resultats_tp["masques"] = resultat

terminer(resultats_tp, dossier_tp_racine, principal="masques")
