"""Atelier 0 : réutiliser un traitement."""


def est_prioritaire(actif: bool, charge: int) -> bool:
    # Les annotations bool/int sont des indications de type, pas des conversions.
    # TODO : renvoyer actif and charge >= 80.
    return False


print(est_prioritaire(True, 90))
print(est_prioritaire(False, 90))
print(est_prioritaire(True, 30))
