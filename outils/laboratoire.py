"""Préparer/arrêter exclusivement les conteneurs du laboratoire PYX."""

import argparse
import json
import socket
import subprocess
import time

from admin_tools.chemins import RACINE

LAB = RACINE / "laboratoire"
CLES = RACINE / ".labo"
COMPOSE = ["docker", "compose", "-f", str(LAB / "compose.yaml")]


def commande(args):
    return subprocess.run(args, check=True, capture_output=True, text=True)


def preparer():
    CLES.mkdir(mode=0o700, exist_ok=True)
    inventaire = CLES / "inventaire.json"
    if (
        inventaire.exists()
        and json.loads(inventaire.read_text()).get("origine") != "docker_secours"
    ):
        raise ValueError(
            "Inventaire personnalisé présent : il est conservé. Utiliser les cibles configurées."
        )
    cle = CLES / "id_ed25519"
    if not cle.exists():
        commande(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(cle)])
    cle.chmod(0o600)
    commande(COMPOSE + ["build"])
    commande(COMPOSE + ["up", "-d", "machine1", "machine2"])
    lignes = []
    for nom, port in [("machine1", 22231), ("machine2", 22232)]:
        deadline = time.monotonic() + 30
        while True:
            try:
                with socket.create_connection(("127.0.0.1", port), timeout=1):
                    pass
                pub = commande(
                    COMPOSE + ["exec", "-T", nom, "cat", "/etc/ssh/ssh_host_ed25519_key.pub"]
                ).stdout.split()
                break
            except (OSError, subprocess.CalledProcessError):
                if time.monotonic() > deadline:
                    raise RuntimeError(f"La cible {nom} ne démarre pas.") from None
                time.sleep(0.3)
        # Clés récupérées par le canal Docker local, pas acceptées aveuglément via SSH.
        lignes.append(f"{nom},[127.0.0.1]:{port} {pub[0]} {pub[1]}")
    (CLES / "known_hosts").write_text("\n".join(lignes) + "\n")
    inventaire.write_text(
        json.dumps(
            {
                "origine": "docker_secours",
                "cle": "id_ed25519",
                "known_hosts": "known_hosts",
                "cibles": [
                    {
                        "nom": nom,
                        "hote": "127.0.0.1",
                        "port": port,
                        "utilisateur": "apprenant",
                        "python": "/usr/local/bin/python3",
                        "dossier_tp": "/home/apprenant/pyx-tp06",
                    }
                    for nom, port in [("machine1", 22231), ("machine2", 22232)]
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("Deux cibles SSH de secours préparées. Ansible s'exécute dans le projet uv du poste.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["preparer", "arreter", "statut"])
    args = parser.parse_args()
    if args.action == "preparer":
        preparer()
    elif args.action == "arreter":
        commande(COMPOSE + ["down"])
        print("Conteneurs PYX arrêtés et supprimés ; aucun autre projet Docker modifié.")
    else:
        print(commande(COMPOSE + ["ps"]).stdout)


if __name__ == "__main__":
    main()
