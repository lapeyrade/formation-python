"""Chemins du kit fourni : aucune donnée personnelle n'est utilisée."""

from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
DONNEES = RACINE / "donnees"
