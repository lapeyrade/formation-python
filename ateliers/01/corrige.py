"""Qualifier un parc fictif avant l'intervention : normaliser, prioriser, dimensionner."""

from ipaddress import ip_network

from admin_tools.atelier import dossier_tp, preparer_etape, terminer
from parc import PARC, MachineNormalisee

dossier_tp_racine = dossier_tp("tp01")
resultats_tp = {}

# === TYPES — Normaliser les données du parc (25 min) ===
dossier = preparer_etape(dossier_tp_racine, "types")
machines: list[MachineNormalisee] = []
for ligne in PARC:
    # On construit une nouvelle ligne pour conserver le parc source et ses types reçus.
    nom = ligne["nom"].strip().lower()
    machines.append(
        {
            **ligne,
            "nom": nom,
            "site": nom.split("-")[1],
            "port": int(ligne["port"]),
            "actif": ligne["actif"] == "oui",
        }
    )
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
machines = []
for ligne in PARC:
    # On construit une nouvelle ligne pour conserver le parc source et ses types reçus.
    nom = ligne["nom"].strip().lower()
    machines.append(
        {
            **ligne,
            "nom": nom,
            "site": nom.split("-")[1],
            "port": int(ligne["port"]),
            "actif": ligne["actif"] == "oui",
        }
    )
prioritaires = [m["nom"] for m in machines if m["actif"] and m["charge"] >= 80]
tentatives = []
for reponses in [[False, True], [False, False, False]]:
    essais, succes = 0, False
    while essais < 3 and not succes:
        # Lire avant d’incrémenter garde l’index valide ; succès et borne limitent la boucle.
        succes = reponses[essais]
        essais += 1
    tentatives.append(essais)
resultat = {
    "prioritaires": prioritaires,
    "inactives": sum(not m["actif"] for m in machines),
    "tentatives": tentatives,
}

resultats_tp["boucles"] = resultat

# === MASQUES — Préparer le plan réseau (40 min) ===
dossier = preparer_etape(dossier_tp_racine, "masques")
machines = []
for ligne in PARC:
    # On construit une nouvelle ligne pour conserver le parc source et ses types reçus.
    nom = ligne["nom"].strip().lower()
    machines.append(
        {
            **ligne,
            "nom": nom,
            "site": nom.split("-")[1],
            "port": int(ligne["port"]),
            "actif": ligne["actif"] == "oui",
        }
    )
masques, capacites = [], []
for prefixe in [24, 27, 29]:
    # Construire 32 bits puis convertir quatre octets relie le préfixe au masque décimal.
    bits = "1" * prefixe + "0" * (32 - prefixe)
    masque = ".".join(str(int(bits[i : i + 8], 2)) for i in range(0, 32, 8))
    reseau = ip_network(f"192.0.2.0/{prefixe}")
    assert masque == str(reseau.netmask)
    masques.append(masque)
    # Valide ici uniquement pour les trois préfixes de cette mission, pas /31 et /32.
    capacites.append(reseau.num_addresses - 2)
resultat = {
    "masques": masques,
    "capacites": capacites,
    "prefixes_invalides": [p for p in [-1, 24, 33] if not 0 <= p <= 32],
    "sites": {site: sum(m["site"] == site for m in machines) for site in ["lyon", "paris"]},
}

resultats_tp["masques"] = resultat

terminer(resultats_tp, dossier_tp_racine, principal="masques")
