"""Atelier 0 : parcourir un petit parc."""

# OBJECTIF : Afficher et compter uniquement les machines actives du parc.
# 1. Dans la boucle `for` fournie, remplacez `pass` par `if machine["actif"]:` (quatre espaces avant `if`).
# 2. Dans ce `if`, écrivez `print(machine["nom"])` (huit espaces avant `print`).
# 3. Toujours dans ce `if`, ajoutez `compteur += 1` avec la même indentation.
# À CONSERVER : Gardez les données, `compteur = 0` avant la boucle et le dernier `print(...)` hors de la boucle.
# Vérification : uv run python ateliers/00/verifier.py 5

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
