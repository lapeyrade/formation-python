class Machine:
    def __init__(self, nom, ip, actif=True):
        # Les attributs appartiennent à cette instance, pas à toutes les machines.
        self.nom = nom
        self.ip = ip
        self.actif = actif

    # La méthode lit cette instance ; changer une autre machine ne modifie pas son état.
    def resume(self):
        # Renvoyer le texte permet au client de choisir où l’afficher ou l’enregistrer.
        return f"{self.nom} | {self.ip} | {'actif' if self.actif else 'inactif'}"
