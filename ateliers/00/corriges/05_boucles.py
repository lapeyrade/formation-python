"""Atelier 0 : parcourir un petit parc."""

parc = [
    {"nom": "srv-web-01", "actif": True},
    {"nom": "srv-db-01", "actif": False},
    {"nom": "srv-backup-01", "actif": True},
]
compteur = 0  # Initialiser une seule fois, avant la boucle.
for machine in parc:
    if machine["actif"]:  # Le champ est déjà un booléen.
        print(machine["nom"])
        compteur += 1  # Compter uniquement les machines retenues.
print(f"Actives : {compteur}")  # Hors de la boucle : bilan final.
