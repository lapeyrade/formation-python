"""Créer une archive de votre projet et de vos résultats, sans environnement ni clés."""

import argparse
import json
import os
import zipfile
from datetime import datetime
from pathlib import Path

from admin_tools.chemins import RACINE

EXCLUS = {".venv", ".labo", ".git", "__pycache__", ".pytest_cache", ".ruff_cache", "node_modules"}
FICHIERS = {"pyproject.toml", "uv.lock", ".python-version", "catalogue.json", "README.md"}
DOSSIERS = {"ateliers", "src", "outils", "docs", "donnees", "laboratoire", "sorties"}


def fichiers_de_connexion():
    """Exclure aussi une configuration active située hors de .labo."""
    chemin = Path(os.environ.get("PYX_INVENTAIRE", RACINE / ".labo/inventaire.json"))
    chemin = chemin.expanduser().resolve()
    fichiers = {chemin}
    try:
        configuration = json.loads(chemin.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return fichiers
    if isinstance(configuration, dict):
        for nom in ["cle", "known_hosts"]:
            valeur = configuration.get(nom)
            if isinstance(valeur, str) and valeur:
                fichier = Path(valeur).expanduser()
                if not fichier.is_absolute():
                    fichier = chemin.parent / fichier
                fichiers.add(fichier.resolve())
    return fichiers


def sauvegarder(destination):
    destination = Path(destination).resolve()
    confidentiels = fichiers_de_connexion()
    selection = []
    for nom in sorted(FICHIERS | DOSSIERS):
        entree = RACINE / nom
        for fichier in sorted(entree.rglob("*")) if entree.is_dir() else [entree]:
            relatif = fichier.relative_to(RACINE)
            if any(p in EXCLUS or p.endswith(".egg-info") for p in relatif.parts):
                continue
            if fichier.name.startswith((".env", "sauvegarde-travail-")):
                continue
            if fichier.name == "inventaire-ansible.json" or fichier.suffix in {".pyc", ".pyo"}:
                continue
            if (
                fichier.is_file()
                and not fichier.is_symlink()
                and fichier.resolve() not in confidentiels | {destination}
            ):
                selection.append((fichier, relatif))
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "x", zipfile.ZIP_DEFLATED) as archive:
        for fichier, relatif in selection:
            archive.write(fichier, Path("formation-python") / relatif)
    with zipfile.ZipFile(destination) as archive:
        if archive.testzip() is not None:
            raise ValueError("L'archive de sauvegarde est endommagée.")
    return len(selection)


def main():
    parseur = argparse.ArgumentParser(description=__doc__)
    nom = f"sauvegarde-travail-{datetime.now():%Y%m%d-%H%M%S}.zip"
    parseur.add_argument("--destination", type=Path, default=RACINE / "sorties" / nom)
    options = parseur.parse_args()
    nombre = sauvegarder(options.destination)
    print(f"{nombre} fichiers sauvegardés : {options.destination}")
    print("Téléchargez cette archive sur votre ordinateur avant la fermeture du poste distant.")


if __name__ == "__main__":
    main()
