"""Atelier 0 : réutiliser un traitement."""

# OBJECTIF : Écrire une fonction qui indique si un serveur est prioritaire.
# 1. Dans `est_prioritaire`, repérez la ligne `return False` : c’est la seule ligne de code à modifier.
# 2. Remplacez `False` par une expression qui combine `actif` et `charge >= 80` avec `and`.
# 3. Gardez `return` et les quatre espaces au début de la ligne : la fonction doit renvoyer le résultat.
# À CONSERVER : Gardez la définition `def ...` et les trois appels `print(est_prioritaire(...))` fournis.
# Vérification : uv run python ateliers/00/verifier.py 6


def est_prioritaire(actif: bool, charge: int) -> bool:
    # Les annotations bool/int sont des indications de type, pas des conversions.
    # TODO : renvoyer actif and charge >= 80.
    return False


print(est_prioritaire(True, 90))
print(est_prioritaire(False, 90))
print(est_prioritaire(True, 30))
