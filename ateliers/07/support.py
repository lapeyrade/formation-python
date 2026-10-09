"""Code fourni de l'atelier 7 : configuration, observation et écriture du rapport.

Aucune installation supplémentaire, connexion SSH ou modification de configuration.
Les fonctions à compléter restent dans depart.py ; ce fichier est à lire si besoin.
"""

import argparse
import configparser
import json
import math
import platform
import shutil
import socket
import sys
import tempfile
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path
from typing import TypedDict


class Observation(TypedDict):
    hostname: str
    date_utc: str
    systeme: str
    chemin_mesure: str
    origine_mesure: str
    total_octets: int
    utilise_octets: int


class AtelierIncomplet(ValueError):
    """Un TODO manque ; expliquer le point à compléter sans afficher de traceback."""


def lire_seuil(chemin: Path) -> int:
    configuration = configparser.ConfigParser(interpolation=None)
    with chemin.open(encoding="utf-8") as fichier:
        configuration.read_file(fichier)
    try:
        seuil = configuration.getint("supervision", "seuil_disque_pct")
    except ValueError as erreur:
        raise ValueError("seuil_disque_pct doit être un entier entre 1 et 100.") from erreur
    if not 1 <= seuil <= 100:
        raise ValueError("seuil_disque_pct doit être un entier entre 1 et 100.")
    return seuil


def observer(chemin: Path, simulation: Path | None) -> Observation:
    if simulation is None:
        disque = shutil.disk_usage(chemin)
        total, utilise = disque.total, disque.used
    else:
        data = json.loads(simulation.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("La simulation doit être un objet JSON avec total et utilise.")
        total, utilise = data.get("total"), data.get("utilise")
    if type(total) is not int or type(utilise) is not int:
        raise ValueError("Les volumes total et utilise doivent être des entiers en octets.")
    if total <= 0 or not 0 <= utilise <= total:
        raise ValueError("Volumes incohérents : total > 0 et 0 <= utilise <= total sont requis.")
    return {
        "hostname": socket.gethostname(),
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "systeme": platform.system(),
        "chemin_mesure": str(chemin),
        "origine_mesure": "simulation" if simulation is not None else "reelle",
        "total_octets": total,
        "utilise_octets": utilise,
    }


def executer(
    calculer: Callable[[int, int], float | None],
    choisir: Callable[[float, int], str | None],
    rapporter: Callable[[Observation, float, int, str], dict[str, object]],
    coder: Callable[[str], int | None],
) -> int:
    parser = argparse.ArgumentParser(description="Contrôler le disque selon supervision.ini.")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path.home() / "pyx-tp06/supervision.ini",
        help="configuration créée au TP6 ; un exemple est fourni dans ateliers/07/donnees",
    )
    parser.add_argument("--chemin", type=Path, default=Path("/"), help="volume à observer")
    parser.add_argument(
        "--simulation", type=Path, help="mesure fictive JSON, sans remplir le disque"
    )
    parser.add_argument("--seuil", type=int, help="remplacer le seuil pour cet essai uniquement")
    parser.add_argument("--sortie", type=Path, help="nouveau fichier JSON ; sinon un essai neuf")
    args = parser.parse_args()
    if args.seuil is not None and not 1 <= args.seuil <= 100:
        parser.error("--seuil doit être un entier entre 1 et 100.")
    try:
        seuil = lire_seuil(args.config)
        if args.seuil is not None:
            seuil = args.seuil
        observation = observer(args.chemin.resolve(), args.simulation)
        pourcentage = calculer(observation["total_octets"], observation["utilise_octets"])
        if pourcentage is None:
            raise AtelierIncomplet("TODO 1 : compléter calculer_pourcentage.")
        if not math.isfinite(pourcentage) or not 0 <= pourcentage <= 100:
            raise ValueError("Le pourcentage calculé doit être compris entre 0 et 100.")
        statut = choisir(pourcentage, seuil)
        if statut not in {"OK", "ALERTE"}:
            raise AtelierIncomplet("TODO 2 : choisir le statut OK ou ALERTE.")
        rapport = rapporter(observation, pourcentage, seuil, statut)
        if rapport.get("statut") is None:
            raise AtelierIncomplet("TODO 3 : conserver le statut dans le rapport.")
        code = coder(statut)
        if code not in {0, 1}:
            raise AtelierIncomplet("TODO 4 : choisir le code de fin 0 ou 1.")
        if args.sortie is None:
            parent = Path(__file__).resolve().parents[2] / "sorties/tp07"
            parent.mkdir(parents=True, exist_ok=True)
            destination = Path(tempfile.mkdtemp(prefix="essai-", dir=parent)) / "rapport.json"
        else:
            destination = args.sortie.resolve()
            destination.parent.mkdir(parents=True, exist_ok=True)
        # Écriture exclusive : un essai ne remplace jamais un rapport existant.
        with destination.open("x", encoding="utf-8") as fichier:
            json.dump(rapport, fichier, ensure_ascii=False, indent=2)
            fichier.write("\n")
        print(f"{statut} : {pourcentage:.2f} % utilisés ; seuil {seuil} %.")
        print("Rapport :", destination)
        return code
    except AtelierIncomplet as erreur:
        print("À compléter :", erreur)
        return 2
    except (OSError, ValueError, configparser.Error) as erreur:
        print("Erreur :", erreur, file=sys.stderr)
        return 2
