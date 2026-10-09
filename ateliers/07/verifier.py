"""Contrôler les quatre étapes de l'atelier 7, séparément ou de bout en bout.

Les simulations et les productions sont isolées dans un dossier temporaire.
Le contrôle ne modifie ni depart.py ni la configuration créée au TP6.
"""

import argparse
import importlib
import json
import math
import os
import platform
import socket
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from types import ModuleType

from support import Observation

RACINE = Path(__file__).resolve().parent
DONNEES = RACINE / "donnees"


def valeur(nom: str, obtenu: object, attendu: object) -> bool:
    conforme = obtenu == attendu
    print(f"{nom} : {'Conforme' if conforme else 'À revoir'}")
    if not conforme:
        print(f"  Attendu : {attendu!r} ; obtenu : {obtenu!r}")
    return conforme


def fonctions(module: ModuleType, etape: str) -> list[bool]:
    controles = []
    if etape == "calcul":
        for total, utilise, attendu in [
            (1000, 420, 42.0),
            (1000, 850, 85.0),
            (1000, 800, 80.0),
            (1000, 0, 0.0),
            (1000, 1000, 100.0),
            (10000, 7996, 79.96),
        ]:
            obtenu = module.calculer_pourcentage(total, utilise)
            conforme = type(obtenu) in {int, float} and math.isclose(
                obtenu, attendu, rel_tol=1e-9, abs_tol=1e-9
            )
            controles.append(valeur(f"calcul {utilise}/{total}", conforme, True))
    elif etape == "decision":
        for pourcentage, seuil, attendu in [
            (42.0, 80, "OK"),
            (85.0, 80, "ALERTE"),
            (80.0, 80, "ALERTE"),
            (79.96, 80, "OK"),
            (85.0, 90, "OK"),
            (42.0, 30, "ALERTE"),
        ]:
            controles.append(
                valeur(
                    f"décision {pourcentage} % / seuil {seuil}",
                    module.choisir_statut(pourcentage, seuil),
                    attendu,
                )
            )
    elif etape == "rapport":
        observation: Observation = {
            "hostname": "vm-exemple",
            "date_utc": "2026-10-09T12:00:00+00:00",
            "systeme": "Linux",
            "chemin_mesure": "/",
            "origine_mesure": "simulation",
            "total_octets": 1000,
            "utilise_octets": 850,
        }
        original = dict(observation)
        attendu = {
            **observation,
            "pourcentage_utilise": 85.0,
            "seuil_disque_pct": 80,
            "statut": "ALERTE",
        }
        controles.append(
            valeur(
                "rapport avec contexte et décision",
                module.construire_rapport(observation, 85.0, 80, "ALERTE"),
                attendu,
            )
        )
        controles.append(valeur("observation originale conservée", observation, original))
    else:
        controles.extend(
            [
                valeur("code OK", module.choisir_code("OK"), 0),
                valeur("code ALERTE", module.choisir_code("ALERTE"), 1),
            ]
        )
        controles.extend(commandes(module.__name__))
    return controles


def commandes(nom_module: str) -> list[bool]:
    controles = []
    script = RACINE / f"{nom_module}.py"
    with tempfile.TemporaryDirectory(prefix="pyx-tp07-") as temporaire:
        dossier = Path(temporaire)
        proche = dossier / "proche.json"
        proche.write_text('{"total": 10000, "utilise": 7996}', encoding="utf-8")
        invalide = dossier / "invalide.json"
        invalide.write_text('{"total": 0, "utilise": 0}', encoding="utf-8")
        mauvaise_config = dossier / "invalide.ini"
        mauvaise_config.write_text("[supervision]\nseuil_disque_pct=101\n", encoding="utf-8")
        exemple = DONNEES / "supervision.exemple.ini"
        avant = exemple.read_bytes()
        cas = [
            ("simulation normale", DONNEES / "disque-normal.json", [], 0, "OK", 42.0, 80),
            ("simulation alerte", DONNEES / "disque-alerte.json", [], 1, "ALERTE", 85.0, 80),
            ("égalité au seuil", DONNEES / "disque-limite.json", [], 1, "ALERTE", 80.0, 80),
            ("seuil relevé", DONNEES / "disque-alerte.json", ["--seuil", "90"], 0, "OK", 85.0, 90),
            (
                "seuil abaissé",
                DONNEES / "disque-normal.json",
                ["--seuil", "30"],
                1,
                "ALERTE",
                42.0,
                30,
            ),
            ("précision avant décision", proche, [], 0, "OK", 79.96, 80),
            ("mesure réelle", None, [], None, None, None, 80),
            (
                "arguments invalides",
                DONNEES / "disque-normal.json",
                ["--seuil", "0"],
                2,
                None,
                None,
                80,
            ),
            ("volume nul refusé", invalide, [], 2, None, None, 80),
            (
                "configuration absente",
                DONNEES / "disque-normal.json",
                ["--config", str(dossier / "absente.ini")],
                2,
                None,
                None,
                80,
            ),
            (
                "seuil INI invalide",
                DONNEES / "disque-normal.json",
                ["--config", str(mauvaise_config)],
                2,
                None,
                None,
                80,
            ),
        ]
        for i, (nom, simulation, options, code, statut, pct, seuil) in enumerate(cas):
            destination = dossier / f"rapport-{i}.json"
            commande = [
                sys.executable,
                "-W",
                "error",
                str(script),
                "--config",
                str(exemple),
                "--sortie",
                str(destination),
                "--chemin",
                str(RACINE),
                *options,
            ]
            if simulation is not None:
                commande.extend(["--simulation", str(simulation)])
            try:
                resultat = subprocess.run(
                    commande,
                    cwd=dossier,
                    capture_output=True,
                    text=True,
                    timeout=5,
                    check=False,
                    env={**os.environ, "PYTHONWARNINGS": "error", "PYTHONIOENCODING": "utf-8"},
                )
                if code == 2:
                    assert resultat.returncode == 2 and resultat.stderr and not destination.exists()
                    assert "Traceback" not in resultat.stderr
                else:
                    assert destination.is_file(), "rapport JSON absent"
                    rapport = json.loads(destination.read_text(encoding="utf-8"))
                    if simulation is None:
                        pct = rapport["utilise_octets"] / rapport["total_octets"] * 100
                        statut = "ALERTE" if pct >= seuil else "OK"
                        code = 1 if statut == "ALERTE" else 0
                        assert 0 <= rapport["utilise_octets"] <= rapport["total_octets"]
                        assert rapport["total_octets"] > 0
                    else:
                        entree = json.loads(simulation.read_text(encoding="utf-8"))
                        assert rapport["total_octets"] == entree["total"]
                        assert rapport["utilise_octets"] == entree["utilise"]
                    assert resultat.returncode == code and not resultat.stderr
                    assert pct is not None and statut is not None
                    assert rapport["statut"] == statut
                    assert math.isclose(rapport["pourcentage_utilise"], pct, abs_tol=1e-9)
                    assert rapport["seuil_disque_pct"] == seuil
                    assert rapport["hostname"] == socket.gethostname()
                    assert rapport["systeme"] == platform.system()
                    assert rapport["chemin_mesure"] == str(RACINE)
                    assert rapport["origine_mesure"] == (
                        "reelle" if simulation is None else "simulation"
                    )
                    assert datetime.fromisoformat(rapport["date_utc"]).utcoffset() is not None
                    assert resultat.stdout.startswith(statut + " :")
                controles.append(valeur(nom, True, True))
            except (
                AssertionError,
                OSError,
                ValueError,
                KeyError,
                TypeError,
                subprocess.TimeoutExpired,
            ) as erreur:
                controles.append(valeur(nom, False, True))
                print("  Détail :", str(erreur) or "relire le rapport et le code de fin")
        # Une seconde écriture doit refuser de remplacer une preuve déjà présente.
        destination = dossier / "rapport-0.json"
        sauvegarde = destination.read_bytes() if destination.exists() else None
        resultat = subprocess.run(
            [
                sys.executable,
                "-W",
                "error",
                str(script),
                "--config",
                str(exemple),
                "--simulation",
                str(DONNEES / "disque-normal.json"),
                "--sortie",
                str(destination),
            ],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        controles.append(
            valeur(
                "rapport existant conservé",
                sauvegarde is not None
                and resultat.returncode == 2
                and destination.read_bytes() == sauvegarde
                and "Traceback" not in resultat.stderr,
                True,
            )
        )
        controles.append(valeur("configuration originale conservée", exemple.read_bytes(), avant))
    return controles


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--corrige", action="store_true", help="contrôler corrige.py sans changer depart.py"
    )
    parser.add_argument(
        "--etape",
        choices=["1", "2", "3", "4", "tous", "calcul", "decision", "rapport", "codes"],
        default="1",
        help="1=Python, 2=déploiement, 3=template, 4=idempotence ; défaut : Python",
    )
    parser.add_argument(
        "--local", action="store_true", help="test Ansible local explicite, sans SSH"
    )
    args = parser.parse_args()
    try:
        module = importlib.import_module("corrige" if args.corrige else "depart")
        controles = []
        if args.etape in {"1", "tous", "calcul", "decision", "rapport", "codes"}:
            etapes_python = (
                ["calcul", "decision", "rapport", "codes"]
                if args.etape in {"1", "tous"}
                else [args.etape]
            )
            for etape in etapes_python:
                controles.extend(fonctions(module, etape))
        if args.etape in {"2", "3", "4", "tous"}:
            from verifier_ansible import verifier

            for etape in ["2", "3", "4"] if args.etape == "tous" else [args.etape]:
                controles.extend(verifier(etape, args.corrige, args.local))
    except Exception as erreur:
        # Le contrôle doit expliquer une faute dans le code en cours d'apprentissage.
        print(f"À revoir : {type(erreur).__name__} : {erreur}")
        return 1
    reussi = bool(controles) and all(controles)
    print(f"Étapes contrôlées : {args.etape}")
    print(f"Atelier 7 — {'OK' if reussi else 'À revoir'}")
    return 0 if reussi else 1


if __name__ == "__main__":
    raise SystemExit(main())
