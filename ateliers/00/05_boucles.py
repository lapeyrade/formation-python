"""Atelier 0 : parcourir un petit parc."""

parc = [
    {"nom": "srv-web-01", "actif": True},
    {"nom": "srv-db-01", "actif": False},
    {"nom": "srv-backup-01", "actif": True},
]
compteur = 0
for machine in parc:
    # TODO : si machine["actif"] est vrai, afficher son nom et incrémenter compteur.
    pass  # Remplacer pass par le bloc if ; pass ne fait rien.
print(f"Actives : {compteur}")
