"""Atelier 0 : prendre une décision."""

actif = True
charge = 85
if not actif:  # Priorité : une machine arrêtée est hors ligne quelle que soit sa charge.
    etat = "hors ligne"
elif charge >= 80:  # Cette branche n'est testée que si la machine est active.
    etat = "alerte"
else:
    etat = "normal"
print(etat)
