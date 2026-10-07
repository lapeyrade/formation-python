"""Atelier 0 : variables et calculs."""

# OBJECTIF : Afficher le nom, la mémoire libre et l’état d’un serveur.
# 1. Remplacez `nom = ""` par une affectation du texte `"srv-web-01"` à `nom`.
# 2. Remplacez le `0` de `ram_libre` par le calcul `ram_totale - ram_utilisee`.
# 3. Remplacez `False` par `True` dans la ligne qui définit `actif`.
# À CONSERVER : Gardez `ram_totale`, `ram_utilisee` et les trois lignes `print(...)` fournis.
# Vérification : uv run python ateliers/00/verifier.py 1

# Une chaîne s'écrit entre guillemets.
nom = ""  # TODO : nommer le serveur srv-web-01.
ram_totale = 16
ram_utilisee = 6
ram_libre = 0  # TODO : calculer la différence avec les deux variables.
actif = False  # TODO : le serveur est actif.
print(nom)
print(ram_libre)
print(actif)
