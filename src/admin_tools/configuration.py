"""Contrat de la configuration de supervision de l'exercice."""

PARAMETRES = {"seuil_disque_pct": 80, "intervalle_s": 60}


def valider_parametres(parametres):
    if set(parametres) != set(PARAMETRES):
        raise ValueError("Paramètres de supervision incomplets.")
    for nom, maximum in [("seuil_disque_pct", 100), ("intervalle_s", 3600)]:
        valeur = parametres[nom]
        if type(valeur) is not int or not 1 <= valeur <= maximum:
            raise ValueError(f"Valeur invalide : {nom}.")
    return dict(parametres)


def contenu_configuration(nom, parametres):
    parametres = valider_parametres(parametres)
    return (
        f"[supervision]\ncible={nom}\n"
        f"seuil_disque_pct={parametres['seuil_disque_pct']}\n"
        f"intervalle_s={parametres['intervalle_s']}\n"
    )
