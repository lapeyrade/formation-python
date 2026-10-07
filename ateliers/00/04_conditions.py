"""Atelier 0 : prendre une décision."""

# OBJECTIF : Calculer un état à partir de l’activité et de la charge du serveur.
# 1. À la place des commentaires TODO, avant `print(etat)`, écrivez un bloc `if not actif:`.
# 2. Dans ce bloc, avec quatre espaces, affectez `"hors ligne"` à `etat`.
# 3. Ajoutez `elif charge >= 80:` au même niveau que `if`, puis affectez `"alerte"` à `etat` dans son bloc.
# 4. Ajoutez `else:` au même niveau que `if`, puis affectez `"normal"` à `etat` dans son bloc.
# À CONSERVER : Gardez `actif = True`, `charge = 85` et `print(etat)` pour le premier contrôle.
# Vérification : uv run python ateliers/00/verifier.py 4

actif = True
charge = 85
etat = "à compléter"
# TODO : if not actif / elif charge >= 80 / else.
# Dans chaque branche, affecter le texte attendu à etat.
print(etat)
