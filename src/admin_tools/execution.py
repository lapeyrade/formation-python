"""Exécution isolée des blocs indépendants des six ateliers."""

import re
import sys
from pathlib import Path

from admin_tools.atelier import terminer


def executer_etape(script, etape, laboratoire=False):
    """Conserver le préambule et le bloc choisi, avec leurs numéros de ligne."""
    script = Path(script).resolve()
    lignes = script.read_text(encoding="utf-8").splitlines(keepends=True)
    reperes = []
    for index, ligne in enumerate(lignes):
        match = re.match(r"# === ([A-Z]+) —", ligne)
        if match:
            reperes.append((index, match[1].lower()))
    choix = next((i for i, (_, nom) in enumerate(reperes) if nom == etape), None)
    if choix is None:
        raise ValueError(f"Bloc introuvable : {etape}")
    debut = reperes[choix][0]
    fin = reperes[choix + 1][0] if choix + 1 < len(reperes) else len(lignes)
    code = "".join(
        ligne
        if (i < reperes[0][0] or debut <= i < fin) and not ligne.startswith("terminer(")
        else "\n"
        for i, ligne in enumerate(lignes)
    )
    contexte = {"__name__": "__main__", "__file__": str(script)}
    argv, chemins = sys.argv[:], sys.path[:]
    try:
        sys.argv = [str(script)] + (["--laboratoire"] if laboratoire else [])
        sys.path.insert(0, str(script.parent))
        exec(compile(code, str(script), "exec"), contexte)
        terminer(contexte["resultats_tp"], contexte["dossier_tp_racine"], principal=etape)
    finally:
        sys.argv, sys.path[:] = argv, chemins
