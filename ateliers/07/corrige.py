"""Correction commentée de l'atelier 7, indépendante de votre fichier depart.py."""

from support import Observation, executer


def calculer_pourcentage(total: int, utilise: int) -> float:
    # La division donne la proportion occupée ; multiplier par 100 donne le pourcentage.
    # Le pilote a déjà refusé un total nul et des volumes incohérents.
    # Garder la précision pour décider : 79.96 reste sous un seuil de 80.
    return utilise / total * 100


def choisir_statut(pourcentage: float, seuil: int) -> str:
    # >= inclut l'égalité : atteindre 80 % suffit à déclencher l'alerte du cours.
    # Une mesure inférieure au seuil reste OK ; elle ne dit rien des autres services.
    if pourcentage >= seuil:
        statut = "ALERTE"
    else:
        statut = "OK"
    return statut


def construire_rapport(
    observation: Observation, pourcentage: float, seuil: int, statut: str
) -> dict[str, object]:
    # **observation copie le contexte dans un nouveau dictionnaire sans modifier l'original.
    # Garder origine_mesure permet de distinguer un essai fictif d'une observation réelle.
    rapport: dict[str, object] = {
        **observation,
        "pourcentage_utilise": pourcentage,
        "seuil_disque_pct": seuil,
        "statut": statut,
    }
    return rapport


def choisir_code(statut: str) -> int:
    # Le code 1 est le contrat de CE script pour une alerte, pas une exception Python.
    # Le code 2 est réservé par le pilote à une erreur d'arguments, de fichier ou de mesure.
    if statut == "ALERTE":
        code = 1
    else:
        code = 0
    return code


if __name__ == "__main__":
    raise SystemExit(
        executer(calculer_pourcentage, choisir_statut, construire_rapport, choisir_code)
    )
