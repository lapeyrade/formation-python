"""Option en direct : seule l'IP publique d'exemple est interrogée."""

import json
import sys

import requests

from admin_tools.atelier import dossier_tp


def main():
    dossier = dossier_tp("geo-directe")
    try:
        reponse = requests.get("https://ipwho.is/8.8.8.8", timeout=10)
        reponse.raise_for_status()
        contenu = reponse.json()
        if not isinstance(contenu, dict) or contenu.get("success") is not True:
            raise ValueError("Localisation indisponible pour cet exemple")
        resultat = {
            "ip": "8.8.8.8",
            "pays": contenu.get("country"),
            "ville": contenu.get("city"),
            "statut": "localisee",
            "source": "ipwho.is_direct",
        }
        if not resultat["pays"]:
            raise ValueError("La réponse ne contient pas de pays")
    except (requests.RequestException, ValueError) as erreur:
        print(f"Service direct indisponible : {erreur}. Utiliser le TP 05 local.", file=sys.stderr)
        return 1
    (dossier / "geolocalisation.json").write_text(
        json.dumps(resultat, ensure_ascii=False, indent=2)
    )
    print(json.dumps(resultat, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
