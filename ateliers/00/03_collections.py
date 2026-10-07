"""Atelier 0 : listes et dictionnaires."""

# OBJECTIF : Ajouter un serveur et retrouver des informations dans deux collections.
# 1. Sous la liste `serveurs`, ajoutez une ligne `serveurs.append(...)` avec le texte `"srv-backup-01"`.
# 2. Remplacez la valeur de `premier` par `serveurs[0]` pour lire le premier élément.
# 3. Remplacez la valeur de `nom_machine` par `machine["nom"]` pour lire la clé `nom`.
# À CONSERVER : Gardez le dictionnaire `machine` et les trois `print(...)` fournis.
# Vérification : uv run python ateliers/00/verifier.py 3

serveurs = ["srv-web-01", "srv-db-01"]
# TODO : ajouter "srv-backup-01" avec serveurs.append(...).
machine = {"nom": "srv-web-01", "port": 22, "actif": True}
premier = ""  # TODO : accéder au premier élément de serveurs.
nom_machine = ""  # TODO : accéder à la clé "nom" de machine.
print(len(serveurs))
print(premier)
print(nom_machine)
