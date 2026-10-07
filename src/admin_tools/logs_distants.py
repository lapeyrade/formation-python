"""Transférer des logs d'exercice par SFTP et conserver leur provenance."""

import hashlib
import json
from pathlib import Path

from admin_tools.distant import connexion
from admin_tools.metier import analyser_logs


def rassembler_logs(fichiers, destination):
    """Concaténer sans trier ni dédupliquer ; borner les lignes de chaque source."""
    manifeste = []
    prochaine_ligne = 1
    with Path(destination).open("xb") as sortie:
        for cible, fichier in fichiers:
            octets = Path(fichier).read_bytes()
            lignes = octets.splitlines(keepends=True)
            for ligne in lignes:
                sortie.write(ligne if ligne.endswith(b"\n") else ligne + b"\n")
            manifeste.append(
                {
                    "cible": cible,
                    "fichier": Path(fichier).name,
                    "octets": len(octets),
                    "sha256": hashlib.sha256(octets).hexdigest(),
                    "lignes": len(lignes),
                    "debut": prochaine_ligne,
                    "fin": prochaine_ligne + len(lignes) - 1,
                }
            )
            prochaine_ligne += len(lignes)
    return manifeste


def telecharger_logs(cibles, inventaire, dossier, journal):
    """L'échec d'un transfert interdit de présenter le regroupement comme complet."""
    repertoire = dossier / "logs"
    repertoire.mkdir()
    fichiers = []
    for cible in cibles:
        local = repertoire / f"{cible['nom']}.log"
        with connexion(cible, inventaire) as client:
            # Borner l'attente de lecture SFTP comme celle des commandes du TP.
            client.sftp().get_channel().settimeout(5)
            client.get(cible["dossier_tp"] + "/auth.log", local=str(local))
        fichiers.append((cible["nom"], local))
        journal.info("log reçu", extra={"etape": "logs", "cible": cible["nom"]})
    manifeste = rassembler_logs(fichiers, dossier / "auth-collecte.log")
    analyse = analyser_logs(dossier / "auth-collecte.log")
    preuve = {"source": "logs_fictifs_distants", "sources": manifeste, "analyse": analyse}
    (dossier / "preuve-logs.json").write_text(
        json.dumps(preuve, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return preuve
