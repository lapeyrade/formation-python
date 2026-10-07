"""Atelier 0 : réutiliser un traitement."""


def est_prioritaire(actif: bool, charge: int) -> bool:
    # and exige que les deux conditions soient vraies.
    # return permet au code appelant de réutiliser le résultat.
    return actif and charge >= 80


print(est_prioritaire(True, 90))  # Active et chargée : True.
print(est_prioritaire(False, 90))  # Inactive : False, même si la charge est élevée.
print(est_prioritaire(True, 30))  # Active mais peu chargée : False.
