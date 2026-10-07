"""Un module importable et exécutable."""


def etiquette(nom):
    return f"Hôte {nom}"


# Ce garde protège la démonstration : importer etiquette ne lance aucune intervention.
if __name__ == "__main__":
    print(etiquette("srv-web"))
