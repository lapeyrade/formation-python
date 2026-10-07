"""Préparer SSH vers cette VM Linux, après activation du service SSH par l'administrateur."""

import getpass
import json
import os
import platform
import shutil
import subprocess
from pathlib import Path

from admin_tools.chemins import RACINE


def preparer():
    if platform.system() != "Linux":
        raise ValueError("Lancer cette préparation dans votre VM Linux, pas sur le Mac ou Windows.")
    for outil in ["ssh", "ssh-keygen"]:
        if not shutil.which(outil):
            raise ValueError(f"Installer le client OpenSSH : {outil} absent.")
    dossier = RACINE / ".labo"
    dossier.mkdir(mode=0o700, exist_ok=True)
    inventaire = dossier / "inventaire.json"
    if inventaire.exists():
        raise ValueError(
            "Un inventaire existe déjà : le conserver ou le déplacer avant préparation."
        )
    cle = dossier / "id_ed25519_local"
    if not cle.exists():
        subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(cle)], check=True)
    publique = cle.with_suffix(".pub").read_text().strip()
    ssh = Path.home() / ".ssh"
    ssh.mkdir(mode=0o700, exist_ok=True)
    ssh.chmod(0o700)
    autorisees = ssh / "authorized_keys"
    lignes = autorisees.read_text().splitlines() if autorisees.exists() else []
    if publique not in lignes:
        with autorisees.open("a") as fichier:
            if lignes:
                fichier.write("\n")
            fichier.write(publique + "\n")
    autorisees.chmod(0o600)
    # La clé publique du serveur est lue localement, sans accepter un scan réseau aveugle.
    cles_hote = sorted(Path("/etc/ssh").glob("ssh_host_*_key.pub"))
    if not cles_hote:
        raise ValueError("Clés d’hôte absentes : faire installer et démarrer le serveur OpenSSH.")
    connus = dossier / "known_hosts_local"
    with connus.open("w") as fichier:
        for chemin in cles_hote:
            champs = chemin.read_text().split()
            fichier.write(f"127.0.0.1 {champs[0]} {champs[1]}\n")
    connus.chmod(0o600)
    utilisateur = getpass.getuser()
    python = Path("/usr/bin/python3")
    if not python.is_file():
        raise ValueError("Python système absent : installer python3 dans la VM.")
    subprocess.run(
        [
            "ssh",
            "-i",
            str(cle),
            "-o",
            "IdentitiesOnly=yes",
            "-o",
            "BatchMode=yes",
            "-o",
            "StrictHostKeyChecking=yes",
            "-o",
            f"UserKnownHostsFile={connus}",
            "-o",
            "ConnectTimeout=5",
            f"{utilisateur}@127.0.0.1",
            "true",
        ],
        check=True,
        timeout=10,
    )
    data = {
        "cle": cle.name,
        "known_hosts": connus.name,
        "cibles": [
            {
                "nom": "vm-locale",
                "hote": "127.0.0.1",
                "port": 22,
                "utilisateur": utilisateur,
                "python": str(python),
                "dossier_tp": str(Path.home() / "pyx-tp06"),
            }
        ],
    }
    # Écriture exclusive : ne jamais remplacer une configuration existante.
    with inventaire.open("x") as fichier:
        json.dump(data, fichier, ensure_ascii=False, indent=2)
        fichier.write("\n")
    os.chmod(inventaire, 0o600)
    print("SSH local vérifié ; inventaire prêt :", inventaire)


if __name__ == "__main__":
    try:
        preparer()
    except (OSError, ValueError, subprocess.SubprocessError) as erreur:
        raise SystemExit(f"À résoudre : {erreur}") from None
