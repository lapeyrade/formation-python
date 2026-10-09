"""Vérifications réelles d'Ansible, dans un essai isolé du déploiement manuel."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from ansible_support import (
    ATELIER,
    PROJET,
    changements,
    creer_derive,
    deploiement,
    lire_configuration,
    lire_kit,
    mettre_support_de_cote,
    passage,
    preparer,
)


def verifier(etape: str, corrige: bool, local: bool) -> list[bool]:
    parent = PROJET / "sorties/tp07/verification"
    parent.mkdir(parents=True, exist_ok=True)
    essai = Path(tempfile.mkdtemp(prefix=f"etape-{etape}-", dir=parent))
    inventaire = preparer(essai / "inventaire-ansible.json", local, corrige)
    data = lire_kit(inventaire)
    # Contrôleur et cible sont cette même VM : un essai peut être lu localement.
    data["all"]["hosts"]["vm-locale"]["dossier_deploiement"] = str(essai / "pyx-tp07-ansible")
    inventaire.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    dossier = deploiement(inventaire)
    sources = ATELIER / "ansible" / ("corrige" if corrige else "")
    deployer = sources / "deployer.yml"
    audit = sources / "audit.yml"
    controles = []

    def confirmer(nom: str, resultat: bool) -> None:
        controles.append(resultat)
        print(f"{nom} : {'Conforme' if resultat else 'À revoir'}")
        if not resultat:
            raise ValueError(nom)

    def lancer(
        nom: str, mode="template", seuil=80, intervalle=60, options=(), playbook=None, code=0
    ):
        resultat = passage(
            inventaire,
            playbook or deployer,
            {"mode_configuration": mode, "seuil_disque_pct": seuil, "intervalle_s": intervalle},
            options,
        )
        (essai / f"{nom}.txt").write_text(resultat.stdout + resultat.stderr, encoding="utf-8")
        if resultat.returncode != code or resultat.stderr:
            print(resultat.stdout[-1800:])
            if resultat.stderr:
                print(resultat.stderr)
        confirmer(nom, resultat.returncode == code and not resultat.stderr)
        return resultat

    try:
        lancer("syntaxe", mode="copie", options=("--syntax-check",))
        lancer("deploiement-initial", mode="copie")
        lire_configuration(dossier, 80)
        confirmer("configuration statique et mode 0640", True)
        confirmer(
            "dossiers privés 0700",
            all(p.stat().st_mode & 0o777 == 0o700 for p in [dossier, dossier / "rapports"]),
        )
        for source, destination in [
            (data["all"]["vars"]["fichier_controle"], "controle_disque.py"),
            (data["all"]["vars"]["fichier_support"], "support.py"),
        ]:
            fichier = dossier / destination
            confirmer(
                f"{destination} copié sans modification, mode 0600",
                fichier.read_bytes() == Path(source).read_bytes()
                and fichier.stat().st_mode & 0o777 == 0o600,
            )
        if etape in {"3", "4"}:
            lancer("template-seuil-80")
            lire_configuration(dossier, 80)
            confirmer("variables rendues dans le template", True)
            lancer("template-seuil-90", seuil=90)
            lire_configuration(dossier, 90)
            confirmer("changement de seuil effectivement déployé", True)
            for seuil, code, statut in [(80, 1, "ALERTE"), (90, 0, "OK")]:
                lancer(f"configuration-pour-python-{seuil}", seuil=seuil)
                rapport = dossier / "rapports" / f"controle-{seuil}.json"
                resultat = subprocess.run(
                    [
                        sys.executable,
                        "-W",
                        "error",
                        str(dossier / "controle_disque.py"),
                        "--config",
                        str(dossier / "supervision.ini"),
                        "--simulation",
                        str(ATELIER / "donnees/disque-alerte.json"),
                        "--sortie",
                        str(rapport),
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=10,
                )
                preuve = json.loads(rapport.read_text(encoding="utf-8"))
                confirmer(
                    f"programme déployé : 85 % / seuil {seuil} -> {statut}",
                    resultat.returncode == code
                    and not resultat.stderr
                    and preuve["statut"] == statut
                    and preuve["seuil_disque_pct"] == seuil
                    and preuve["origine_mesure"] == "simulation",
                )
            fichier = dossier / "supervision.ini"
            avant = fichier.read_bytes(), fichier.stat().st_mode
            lancer("seuil-invalide-refuse", seuil=101, code=2)
            confirmer(
                "configuration conservée après un paramètre invalide",
                avant == (fichier.read_bytes(), fichier.stat().st_mode),
            )
            lancer("seuil-texte-refuse", seuil="80", code=2)
            confirmer(
                "configuration conservée après une erreur de type",
                avant == (fichier.read_bytes(), fichier.stat().st_mode),
            )
            lancer("intervalle-120", intervalle=120)
            lire_configuration(dossier, 80, intervalle=120)
            confirmer("intervalle rendu dans la configuration", True)
            lancer("retour-seuil-80")
            lire_configuration(dossier, 80)
        if etape == "4":
            lancer("audit-initial", playbook=audit)
            second = lancer("second-passage")
            confirmer("idempotence : changed=0", changements(second.stdout) == 0)
            sauvegarde = creer_derive(dossier)
            confirmer("sauvegarde de la dérive conservée", sauvegarde.is_file())
            lancer("audit-detecte-derive", playbook=audit, code=2)
            fichier = dossier / "supervision.ini"
            avant = fichier.read_bytes(), fichier.stat().st_mode
            apercu = lancer("apercu-reparation", options=("--check", "--diff"))
            confirmer(
                "aperçu prédit un changement",
                changements(apercu.stdout) > 0,
            )
            confirmer(
                "aperçu conserve contenu et permissions",
                avant == (fichier.read_bytes(), fichier.stat().st_mode),
            )
            reparation = lancer("reparation")
            confirmer("réparation applique un changement", changements(reparation.stdout) > 0)
            lire_configuration(dossier, 80)
            confirmer("seuil 80 et mode 0640 réellement rétablis", True)
            lancer("audit-apres-reparation", playbook=audit)
            copie = mettre_support_de_cote(dossier)
            confirmer("fichier absent conservé dans une sauvegarde", copie.is_file())
            lancer("audit-detecte-fichier-absent", playbook=audit, code=2)
            apercu = lancer("apercu-fichier-absent", options=("--check", "--diff"))
            confirmer(
                "aperçu prédit la copie sans restaurer le fichier",
                changements(apercu.stdout) > 0 and not (dossier / "support.py").exists(),
            )
            restauration = lancer("restauration-fichier-absent")
            confirmer(
                "fichier restauré depuis la source, mode 0600",
                changements(restauration.stdout) > 0
                and (dossier / "support.py").read_bytes() == copie.read_bytes()
                and (dossier / "support.py").stat().st_mode & 0o777 == 0o600,
            )
            lancer("audit-apres-restauration", playbook=audit)
            final = lancer("dernier-passage")
            confirmer("état final stable : changed=0", changements(final.stdout) == 0)
    except (
        OSError,
        ValueError,
        KeyError,
        TypeError,
        AssertionError,
        subprocess.SubprocessError,
    ) as erreur:
        print("À revoir :", str(erreur) or "relire la configuration et les journaux")
        if not controles or all(controles):
            controles.append(False)
    bilan = {"etape": etape, "conforme": bool(controles) and all(controles), "controles": controles}
    (essai / "bilan.json").write_text(json.dumps(bilan, indent=2) + "\n", encoding="utf-8")
    print("Preuves de ce contrôle :", essai)
    return controles
