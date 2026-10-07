"""Générateur guidé : deux TODO ; validation des entrées déjà fournie."""

from ipaddress import ip_address, ip_network


def generer_ips(reseau, reservees=(), limite=None):
    # La validation refuse les cas hors contrat avant de produire des candidates.
    if limite is not None and (type(limite) is not int or limite < 0):
        raise ValueError("limite doit être un entier positif ou nul")
    net = ip_network(reseau)
    if net.version != 4:
        raise ValueError("Le plan de ce laboratoire est IPv4")
    exclusions = {ip_address(ip) for ip in reservees}
    if any(ip not in net for ip in exclusions):
        raise ValueError("Réservation hors du réseau")
    if limite == 0:
        return
    nombre = 0
    for adresse in net.hosts():
        # TODO 1 : si adresse appartient à exclusions, passer à la suivante avec continue.
        # TODO 2 : remplacer yield from () par yield str(adresse).
        # yield suspend le parcours ; la prochaine demande reprend juste après.
        yield from ()
        nombre += 1
        if limite is not None and nombre >= limite:
            return  # La limite porte sur le nombre réellement produit, pas sur les exclusions.
