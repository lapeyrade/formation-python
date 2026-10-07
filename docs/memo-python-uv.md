# Mémo Python et uv

[Accueil](../README.md) - [Glossaire](#glossaire) - [Dépannage](depannage.md) -
[Exploiter un script](exploiter-script.md)

## Exécuter dans le bon projet

Depuis le dossier contenant pyproject.toml :

```sh
uv sync --locked
uv run python outils/diagnostic.py
uv run python ateliers/01/depart.py
uv run python outils/verifier.py tp01 --etape types
```

uv sync prépare l’environnement verrouillé ; uv run utilise celui du projet. Conserver pyproject.toml et uv.lock. Pour
ajouter une dépendance volontairement : uv add NOM. Le cours fournit un wheel local pour pratiquer sans dépendre d’un
téléchargement extérieur.

## Types et conversions

```python
charge = int("85")
actif = "oui" == "oui"
nom = " SRV-PARIS-WEB-01 ".strip().lower()
machine = {"nom": nom, "charge": charge, "actif": actif}
prioritaire = machine["actif"] and machine["charge"] >= 80
```

Une chaîne non vide est vraie : bool("non") vaut True. Valider explicitement oui/non. Le texte d’un CSV se convertit
avant les calculs ; une conversion impossible peut lever ValueError.

## Parcourir et transformer

```python
parc = [{"nom": "srv-a", "actif": True}, {"nom": "srv-b", "actif": False}]
actives = [machine["nom"] for machine in parc if machine["actif"]]
for nom in actives:
    print(nom)
```

Une liste garde des valeurs disponibles pour plusieurs parcours. Un générateur produit à la demande et se consomme ; le
recréer pour recommencer. Un dictionnaire associe des clés à des valeurs. Choisir la structure selon les accès
nécessaires.

## Fonctions et références

```python
def ajouter_service(services, service):
    return [*services, service]


original = ["ssh"]
copie = ajouter_service(original, "https")
```

return fournit un résultat réutilisable ; print l’affiche. L’affectation copie une référence, pas une collection. Une
copie superficielle conserve les références imbriquées. Pour un paramètre par défaut mutable, utiliser None puis créer
une nouvelle collection à chaque appel.

## Chemins, texte et octets

```python
from pathlib import Path

source = Path("donnees/message.txt")
with source.open(encoding="utf-8") as fichier:
    texte = fichier.read()
octets = source.read_bytes()
```

Un chemin relatif dépend du dossier courant. Donner un encodage au texte ; lire le binaire comme des octets. with ferme
le fichier même si le traitement échoue. csv traite les champs cités ; split ne remplace pas un lecteur CSV.

## Erreurs et débogage

1. Lire le type et le message à la fin du traceback.
2. Retrouver la dernière ligne de son propre code.
3. Examiner la valeur, son type et le chemin réellement utilisé.
4. Corriger une cause, puis relancer le même cas et un cas valide.

```sh
uv run python ateliers/02/debogage.py --cas type
uv run python ateliers/02/debogage.py --cas chemin
uv run python ateliers/02/debogage.py --cas type --corrige
```

Ces deux cas affichent volontairement une erreur capturée. Pour s’exercer, modifier prioritaire ou lire_note dans le
fichier, puis relancer sans --corrige. Dans un script métier, traiter les exceptions prévues et conserver les erreurs
inattendues visibles.

## Outils et preuves

| Besoin | Outil | Preuve à relire |
| --- | --- | --- |
| Arguments du script | argparse | Aide, paramètres et code retour |
| Tables du parc | Pandas | Colonnes, unicité, lignes et totaux |
| Conservation | SQLite | Transaction, lignes et sélection |
| API | requests | Délai, statut, format et champs |
| HTML | Scrapy | Sélecteurs et valeurs manquantes |
| Collecte SSH | Fabric | Une mesure ou une erreur par cible |
| État distant | Ansible | Aperçu, contenu, permissions et répétition |
| Archive et message | zipfile/tarfile, email | Membres et octets reçus |

<a id="glossaire"></a>

## Glossaire Python et système

Ces cinq couples distinguent des notions proches. Chaque exemple renvoie à une situation du cours.

| Terme | Définition | Exemple dans les TP |
| --- | --- | --- |
| **Contrôleur** | Machine depuis laquelle on lance la collecte ou la configuration des autres machines. | Au TP06, le poste Linux de formation exécute Fabric et Ansible. |
| **Cible** | Machine distante sur laquelle le contrôleur exécute une commande ou applique une configuration. | Au TP06, la cible SSH locale fournissent leurs mesures et reçoivent supervision.ini. |
| **Module** | Unité de code que Python peut importer, souvent un fichier .py. | Au TP02, inventaire_module.py expose une fonction sans lancer sa démonstration à l’import. |
| **Bibliothèque** | Ensemble de code réutilisable pouvant regrouper plusieurs modules et packages. | Au TP03, ma_boite fournit les règles réseau et la classe Machine aux deux scripts clients. |
| **Exception** | Événement qui interrompt le déroulement normal du code ; elle peut être traitée ou se propager. | Au TP02, comparer la charge texte à un entier lève TypeError. |
| **Code retour** | Entier communiqué à la fin d’un programme au processus qui l’a lancé ; son sens dépend du contrat du programme. | Le client analyse_logs.py renvoie 0 après traitement, 1 si la source est inaccessible et 2 pour un argument invalide. |
| **Transaction** | Ensemble d’écritures en base validées ensemble ou annulées si le traitement échoue avant validation. | Au TP05, une erreur d’insertion provoque le rollback de l’import SQLite. |
| **Idempotence** | Propriété d’une opération dont la répétition avec les mêmes paramètres conserve l’état obtenu au premier passage. | Au TP06, le second passage du playbook doit conserver le contenu et les permissions, avec zéro changement. |
| **Journal technique** | Trace du déroulement d’une exécution : date, niveau, étape, cible et erreurs éventuelles. | execution.log permet de retrouver une collecte réussie ou une erreur par cible. |
| **Rapport métier** | Résultat organisé pour comprendre le parc ou les incidents et décider de la suite. | rapport_complet.csv conserve les compteurs d’échecs et les informations d’inventaire, y compris les inconnues. |

Une exception traitée ne détermine pas à elle seule le code retour du programme. Une transaction protège un groupe
d’écritures ; l’idempotence concerne les effets d’une répétition. Un journal technique aide à diagnostiquer le
traitement ; le rapport présente les données utiles à l’analyse.

## Retrouver et récupérer son travail

```sh
uv run python outils/sauvegarder.py
```

Télécharger l’archive annoncée sur son ordinateur et vérifier son ouverture. Elle conserve le code et les résultats ;
l’environnement et les clés restent exclus. Voir [utilisation](utilisation.md#sauvegarder).
