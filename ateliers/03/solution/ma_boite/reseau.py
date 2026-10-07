import ipaddress


def generer_ips(reseau, reservees=(), limite=None):
    """Adresses candidates non réservées ; aucune sonde ne prouve leur disponibilité."""
    if limite is not None and (type(limite) is not int or limite < 0):
        raise ValueError("limite doit être un entier positif ou nul")
    net = ipaddress.ip_network(reseau)
    if net.version != 4:
        raise ValueError("Le plan de ce laboratoire est IPv4")
    # Comparer des objets IP normalisés évite de mélanger texte et adresses.
    reservees = {ipaddress.ip_address(ip) for ip in reservees}
    if any(ip not in net for ip in reservees):
        raise ValueError("Réservation hors du réseau")
    if limite == 0:
        return
    nombre = 0
    for adresse in net.hosts():
        if adresse in reservees:
            continue
        # Suspendre après une candidate garde une consommation à la demande.
        yield str(adresse)
        # Seules les adresses produites comptent vers la limite, jamais les exclusions.
        nombre += 1
        if limite is not None and nombre >= limite:
            return
