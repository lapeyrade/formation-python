"""Atelier 0 : listes et dictionnaires."""

serveurs = ["srv-web-01", "srv-db-01"]
serveurs.append("srv-backup-01")  # append modifie la liste, sans la réaffecter.
machine = {"nom": "srv-web-01", "port": 22, "actif": True}
premier = serveurs[0]  # Les indices commencent à zéro.
nom_machine = machine["nom"]  # Une clé donne accès à sa valeur.
print(len(serveurs))
print(premier)
print(nom_machine)
