"""Atelier 0 : nettoyer et convertir du texte."""

# OBJECTIF : Transformer des données textuelles en un nom propre et un port numérique.
# 1. Sur la ligne `nom = ...`, appliquez `.strip().lower()` à `nom_brut`.
# 2. Sur la ligne `port = ...`, remplacez `0` par `int(port_brut)`.
# 3. Sur la ligne `message = ...`, écrivez une f-string qui assemble `nom`, le caractère `:` et `port`.
# À CONSERVER : Gardez les données brutes et les trois `print(...)`. La deuxième ligne affiche volontairement `port + 1`, soit 23.
# Vérification : uv run python ateliers/00/verifier.py 2

nom_brut = "  SRV-WEB-01  "
port_brut = "22"
nom = nom_brut  # TODO : retirer les espaces puis passer en minuscules.
port = 0  # TODO : convertir port_brut avec int(...).
message = ""  # TODO : f-string au format srv-web-01:22.
print(nom)
print(port + 1)  # Fourni : ce calcul vérifie que port est un entier.
print(message)
