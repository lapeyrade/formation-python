"""TP 03 — constructeur fourni ; compléter uniquement la méthode de résumé."""


class Machine:
    def __init__(self, nom, ip, actif=True):
        self.nom = nom
        self.ip = ip
        self.actif = actif

    def resume(self):
        # TODO 1 : choisir le texte actif/inactif selon self.actif.
        # TODO 2 : renvoyer une f-string : nom | ip | état.
        # Utiliser self.nom et self.ip : chaque instance garde ses propres attributs.
        return None
