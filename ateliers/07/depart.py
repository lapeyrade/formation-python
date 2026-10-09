"""Atelier 7 optionnel : utiliser la configuration du TP6 pour surveiller le disque.

VOTRE TRAVAIL : les quatre TODO ci-dessous, dans l'ordre du README.
FOURNI : lecture INI, mesure réelle ou simulée, arguments et écriture JSON dans support.py.
Les annotations de types sont déjà écrites ; conservez-les.
"""

from support import Observation, executer


# === 1. CALCUL — du nombre d'octets au pourcentage ===
def calculer_pourcentage(total: int, utilise: int) -> float | None:
    """Exemple : total=1000 et utilise=420 doivent donner 42.0."""
    # Les valeurs sont validées par le code fourni : total > 0, 0 <= utilise <= total.
    # TODO 1 : remplacer None par utilise / total * 100. Ne pas arrondir ici.
    pourcentage: float | None = None
    return pourcentage


# === 2. DECISION — appliquer le seuil de supervision ===
def choisir_statut(pourcentage: float, seuil: int) -> str | None:
    """ALERTE si le pourcentage atteint ou dépasse le seuil, OK sinon."""
    # TODO 2 : remplacer cette ligne par un if/else qui affecte "ALERTE" ou "OK" à statut.
    # Exemple : pourcentage=85.0 et seuil=80 donnent "ALERTE".
    # À la limite, pourcentage=80.0 et seuil=80 donnent aussi "ALERTE".
    statut: str | None = None
    return statut


# === 3. RAPPORT — conserver la décision avec son contexte ===
def construire_rapport(
    observation: Observation, pourcentage: float, seuil: int, statut: str
) -> dict[str, object]:
    """Le contexte est fourni ; compléter seulement la valeur de statut."""
    rapport: dict[str, object] = {
        **observation,  # Fourni : machine, date UTC, chemin, origine et volumes.
        "pourcentage_utilise": pourcentage,
        "seuil_disque_pct": seuil,
        # TODO 3 : remplacer None par la variable statut reçue par cette fonction.
        "statut": None,
    }
    return rapport


# === 4. CODE DE FIN — rendre la décision lisible par un autre programme ===
def choisir_code(statut: str) -> int | None:
    """Ce script retourne 0 pour OK, 1 pour ALERTE ; les erreurs sont gérées à part."""
    if statut == "ALERTE":
        # TODO 4 : remplacer None par 1. Une alerte est une mesure réussie avec seuil dépassé.
        code: int | None = None
    else:
        code = 0
    return code


if __name__ == "__main__":
    # Fourni : ce pilote appelle vos quatre fonctions, puis écrit le rapport.
    raise SystemExit(
        executer(calculer_pourcentage, choisir_statut, construire_rapport, choisir_code)
    )
