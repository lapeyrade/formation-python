"""Préparation et contrôles fournis : une VM, un dossier dédié, aucune nouvelle clé."""

import configparser
import getpass
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from admin_tools.distant import charger_inventaire

ATELIER = Path(__file__).resolve().parent
PROJET = ATELIER.parents[1]
KIT = PROJET / "sorties/tp07/ansible/inventaire-ansible.json"


def preparer(destination: Path, local: bool = False, corrige: bool = False) -> Path:
    """Réutiliser SSH du TP6 ou choisir explicitement le mode sans SSH pour le test."""
    dossier = destination.resolve().parent
    dossier.mkdir(parents=True, exist_ok=True)
    cible = {
        "ansible_host": "127.0.0.1",
        "ansible_user": getpass.getuser(),
        "ansible_python_interpreter": sys.executable,
        "dossier_deploiement": str(Path.home() / "pyx-tp07-ansible"),
    }
    variables = {}
    if local:
        cible["ansible_connection"] = "local"
    else:
        inventaire = charger_inventaire()
        cibles = inventaire["cibles"]
        if len(cibles) != 1 or cibles[0]["hote"] != "127.0.0.1":
            raise ValueError("Cet atelier attend une seule VM, joignable par SSH sur 127.0.0.1.")
        poste = cibles[0]
        if poste["utilisateur"] != getpass.getuser():
            raise ValueError("Exécuter depuis la VM avec le même compte que celui du TP6.")
        cible.update(
            ansible_port=poste["port"],
            ansible_python_interpreter=poste["python"],
        )
        variables = {
            "ansible_ssh_private_key_file": inventaire["cle"],
            "ansible_ssh_common_args": (
                f"-o UserKnownHostsFile={shlex.quote(inventaire['known_hosts'])} "
                "-o IdentitiesOnly=yes -o StrictHostKeyChecking=yes"
            ),
        }
    variables.update(
        fichier_controle=str(ATELIER / ("corrige.py" if corrige else "depart.py")),
        fichier_support=str(ATELIER / "support.py"),
        fichier_config_exemple=str(ATELIER / "donnees/supervision.exemple.ini"),
        fichier_modele=str(
            ATELIER
            / "ansible"
            / ("corrige/templates" if corrige else "templates")
            / "supervision.ini.j2"
        ),
    )
    # Écriture atomique : l'inventaire du TP6 et les sources ne sont jamais remplacés.
    temporaire = dossier / "inventaire.tmp"
    temporaire.write_text(
        json.dumps({"all": {"hosts": {"vm-locale": cible}, "vars": variables}}, indent=2) + "\n",
        encoding="utf-8",
    )
    temporaire.chmod(0o600)
    temporaire.replace(destination)
    return destination


def lire_kit(chemin: Path) -> dict:
    data = json.loads(chemin.read_text(encoding="utf-8"))
    hote = data["all"]["hosts"]
    if set(hote) != {"vm-locale"} or hote["vm-locale"]["ansible_host"] != "127.0.0.1":
        raise ValueError("Conserver la cible unique vm-locale sur 127.0.0.1.")
    return data


def deploiement(chemin: Path) -> Path:
    dossier = Path(lire_kit(chemin)["all"]["hosts"]["vm-locale"]["dossier_deploiement"])
    if not dossier.is_absolute() or dossier.name != "pyx-tp07-ansible" or ".." in dossier.parts:
        raise ValueError("Le dossier dédié doit être un chemin absolu vers pyx-tp07-ansible.")
    return dossier


def passage(inventaire: Path, playbook: Path, variables: dict, options=()):
    """Lancer Ansible et conserver les avertissements éventuels, sans les masquer."""
    if shutil.which("ansible-playbook") is None:
        raise ValueError("Ansible absent : lancer uv sync --locked dans la VM Linux.")
    fichiers = inventaire.parent
    env = {
        **os.environ,
        "ANSIBLE_CONFIG": str(PROJET / "laboratoire/ansible.cfg"),
        "ANSIBLE_NOCOLOR": "1",
        "ANSIBLE_STDOUT_CALLBACK": "default",
        "ANSIBLE_LOCAL_TEMP": str(fichiers / "tmp-controleur"),
        "ANSIBLE_REMOTE_TEMP": str(deploiement(inventaire).parent / ".ansible-tp07"),
    }
    return subprocess.run(
        [
            "ansible-playbook",
            "-i",
            str(inventaire),
            str(playbook),
            "-e",
            json.dumps(variables),
            *options,
        ],
        capture_output=True,
        text=True,
        check=False,
        timeout=90,
        env=env,
    )


def changements(sortie: str) -> int:
    trouve = re.search(
        r"^vm-locale\s*:\s*ok=\d+\s+changed=(\d+)\s+unreachable=0\s+failed=0",
        sortie,
        re.M,
    )
    if trouve is None:
        raise ValueError("Le récapitulatif Ansible ne confirme pas une exécution complète.")
    return int(trouve[1])


def lire_configuration(dossier: Path, seuil: int, intervalle: int = 60) -> None:
    fichier = dossier / "supervision.ini"
    configuration = configparser.ConfigParser(interpolation=None)
    configuration.read(fichier, encoding="utf-8")
    assert configuration.getint("supervision", "seuil_disque_pct") == seuil, "Seuil incorrect"
    assert configuration.getint("supervision", "intervalle_s") == intervalle, "Intervalle incorrect"
    assert configuration.get("supervision", "cible") == "vm-locale", "Cible incorrecte"
    assert fichier.stat().st_mode & 0o777 == 0o640, "Permissions INI attendues : 0640"


def creer_derive(dossier: Path) -> Path:
    """Modifier uniquement le faux fichier de supervision du dossier dédié."""
    if dossier.name != "pyx-tp07-ansible":
        raise ValueError("La dérive est réservée au dossier pyx-tp07-ansible.")
    fichier = dossier / "supervision.ini"
    if fichier.is_symlink():
        raise ValueError("Refus de modifier une configuration qui est un lien symbolique.")
    original = fichier.read_text(encoding="utf-8")
    remplace, nombre = re.subn(r"(?m)^seuil_disque_pct\s*=.*$", "seuil_disque_pct=10", original)
    if nombre != 1:
        raise ValueError("Retrouver une ligne unique seuil_disque_pct avant la dérive.")
    sauvegardes = dossier / "sauvegardes"
    sauvegardes.mkdir(exist_ok=True)
    copie = Path(tempfile.mkdtemp(prefix="avant-derive-", dir=sauvegardes)) / "supervision.ini"
    shutil.copy2(fichier, copie)
    copie.chmod(0o600)
    fichier.write_text(remplace, encoding="utf-8")
    fichier.chmod(0o600)
    return copie


def mettre_support_de_cote(dossier: Path) -> Path:
    """Simuler un fichier absent en le déplaçant, sans le supprimer."""
    if dossier.name != "pyx-tp07-ansible":
        raise ValueError("L'incident est réservé au dossier pyx-tp07-ansible.")
    fichier = dossier / "support.py"
    if fichier.is_symlink() or not fichier.is_file():
        raise ValueError("Retrouver le fichier support.py déployé avant cet incident.")
    sauvegardes = dossier / "sauvegardes"
    sauvegardes.mkdir(exist_ok=True)
    copie = Path(tempfile.mkdtemp(prefix="fichier-absent-", dir=sauvegardes)) / "support.py"
    fichier.replace(copie)
    return copie
