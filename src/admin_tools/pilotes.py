"""Pilotes fournis pour exécuter les essais des TP sans modifier leur code métier."""

import json
import os
import subprocess
import sys

from admin_tools.chemins import DONNEES
from admin_tools.labo import serveur_http


def projet_uv(module_inventaire, dossier):
    """Créer le projet isolé et tester le module indiqué."""
    # Le projet d'essai a son propre environnement ; ne pas lui imposer celui du cours.
    env_uv = os.environ.copy()
    env_uv.pop("VIRTUAL_ENV", None)
    projet = dossier / "projet_uv"
    subprocess.run(
        [
            "uv",
            "init",
            "--bare",
            "--vcs",
            "none",
            "--no-workspace",
            "--python",
            "3.13.13",
            str(projet),
        ],
        check=True,
        capture_output=True,
        text=True,
        env=env_uv,
    )
    (projet / "inventaire_module.py").write_text(
        module_inventaire.read_text(encoding="utf-8"), encoding="utf-8"
    )
    r = subprocess.run(
        [
            sys.executable,
            "-c",
            "import inventaire_module; print(inventaire_module.etiquette('srv-web'))",
        ],
        cwd=projet,
        check=True,
        capture_output=True,
        text=True,
        env=env_uv,
    )
    subprocess.run(
        [
            "uv",
            "add",
            "--project",
            str(projet),
            "--offline",
            str(DONNEES / "wheels" / "pyx_parc-1.0.0-py3-none-any.whl"),
        ],
        check=True,
        capture_output=True,
        text=True,
        env=env_uv,
    )
    subprocess.run(
        [
            "uv",
            "run",
            "--project",
            str(projet),
            "--offline",
            "python",
            "-W",
            "error",
            "-c",
            "import pyx_parc; assert pyx_parc.normaliser_nom(' SRV-WEB ') == 'srv-web'",
        ],
        check=True,
        capture_output=True,
        text=True,
        env=env_uv,
    )
    resultat = {
        "etiquette": r.stdout.strip(),
        "projet": (projet / "pyproject.toml").exists(),
        "verrouillage": (projet / "uv.lock").exists(),
        "environnement": (projet / ".venv").exists(),
    }

    return resultat


def clients_bibliotheque(clients, dossier, ips, machines):
    """Exécuter les deux clients et comparer leurs sorties réelles."""
    resultat = None
    textes = []
    for nom_client in ["generer", "resumer"]:
        execution = subprocess.run(
            [sys.executable, "-W", "error", str(clients / f"{nom_client}.py")],
            check=True,
            capture_output=True,
            text=True,
        )
        if execution.stderr:
            raise RuntimeError(execution.stderr)
        (dossier / f"{nom_client}.txt").write_text(execution.stdout, encoding="utf-8")
        textes.append(execution.stdout.splitlines())
    if len(machines) == 6 and machines[0].resume() is not None:
        resultat = {
            "nombre": len(machines),
            "premier": machines[0].resume(),
            "dernier": machines[-1].resume(),
            "clients_identiques": textes == [ips, [m.resume() for m in machines]],
        }

    return resultat


def verifier_arguments(outil, dossier):
    """Essayer le cas valide, l’aide et trois erreurs de saisie."""
    command = [sys.executable, str(outil)]
    essai = subprocess.run(
        command + [str(DONNEES / "auth.log"), "--seuil", "2", "--sortie", str(dossier)],
        check=False,
        capture_output=True,
        text=True,
    )
    if essai.returncode not in (0, 2):
        essai.check_returncode()
    if essai.returncode == 0 and essai.stderr:
        raise RuntimeError(essai.stderr)
    codes = []
    for args in [
        ["--help"],
        [str(DONNEES / "auth.log"), "--seuil", "abc"],
        [str(DONNEES / "auth.log"), "--seuil", "0"],
        [str(dossier / "absent.log")],
    ]:
        r = subprocess.run(command + args, capture_output=True, text=True)
        codes.append(r.returncode)
    if essai.returncode != 0:
        return None
    resultat = {
        "codes_help_invalide_zero_absent": codes,
        "rapport_cree": (dossier / "compteurs.json").exists(),
    }

    return resultat


def collecter_html(spider, dossier):
    """Lancer le spider sur le serveur local et relire sa production."""
    with serveur_http() as url:
        execution = subprocess.run(
            [
                sys.executable,
                "-W",
                "error",
                str(spider),
                url + "/machines",
                str(dossier / "machines.json"),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        if execution.stderr:
            raise RuntimeError(execution.stderr)
    lignes = json.loads((dossier / "machines.json").read_text(encoding="utf-8"))
    if lignes and all(
        ligne.get("site") and ligne.get("etat") and ligne.get("message") for ligne in lignes
    ):
        return {
            "nombre": len(lignes),
            "sites": [ligne["site"] for ligne in lignes],
            "a_examiner": [ligne["nom"] for ligne in lignes if ligne["etat"] != "OK"],
            "message_absent": lignes[-1]["message"],
        }
    return None
