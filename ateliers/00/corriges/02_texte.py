"""Atelier 0 : nettoyer et convertir du texte."""

nom_brut = "  SRV-WEB-01  "
port_brut = "22"
nom = nom_brut.strip().lower()  # Chaque méthode renvoie une chaîne.
port = int(port_brut)  # La conversion rend possible une addition numérique.
message = f"{nom}:{port}"  # Les accolades insèrent les valeurs.
print(nom)
print(port + 1)
print(message)
