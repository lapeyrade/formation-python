# Mémo Python et administration système

Version du **9 octobre 2026**. Repères pour reprendre les ateliers ; les exemples restent volontairement courts.

[Accueil](../README.md) - [Glossaire](#glossaire) -
[Dépannage](depannage.md) - [Réutiliser un script](exploiter-script.md)

## 1. Exécuter et vérifier dans le bon projet

Toutes les commandes se lancent depuis le dossier contenant `pyproject.toml` et `uv.lock`.
Le terminal exécute sur la machine où il est ouvert : ordinateur personnel et VM sont deux environnements.

```sh
uv sync --locked
uv run python outils/diagnostic.py
uv run python outils/bienvenue.py
```

`uv sync --locked` prépare `.venv` avec les dépendances verrouillées. `uv run` utilise le Python du projet.
Dans VS Code, sélectionner `.venv/bin/python`. Un ancien venv actif peut être différent de cet environnement.
Ne copiez pas `.venv` d’une machine à l’autre ; recréez-le depuis le projet avec uv.

**Pour avancer :** lire le README, ouvrir le fichier indiqué, compléter un TODO, enregistrer, exécuter puis contrôler.
Exemple pour le premier TP :

```sh
uv run python outils/executer_etape.py tp01 types
uv run python outils/verifier.py tp01 --etape types
```

`Conforme` signifie que le contrôle de cette étape passe. `À revoir` est normal tant que le code manque.
Ouvrir les fichiers dans le **dernier dossier d’essai annoncé** ; les chemins changent à chaque lancement.

| Atelier | Ce que vous apprenez à produire |
| --- | --- |
| 0 | Petits programmes pour lire la syntaxe Python |
| 1 et 2 | Inventaire normalisé, sélection, masques et import fiable |
| 3 et 4 | IP candidates, diagnostic et rapport d’incidents |
| 5 et 6 | Base SQLite, enrichissement, archive, collecte et message capturé |
| 7 optionnel | Décision disque à partir du seuil déployé au TP6 |

Les corrigés sont à comparer après votre essai. Ajouter `--corrige` au vérificateur ne remplace pas votre code.
`uv run python outils/verifier.py tous` contrôle les étapes principales ; le TP6 complet avec SSH et l’atelier 7
ont leurs commandes dédiées.

## 2. Lire les données et les structures de contrôle

| Type | Exemple | À retenir |
| --- | --- | --- |
| `str` | `"srv-web"` | Texte ; `strip`, `lower`, `split` renvoient un résultat |
| `int`, `float` | `22`, `42.5` | Nombres ; convertir le texte avant de calculer |
| `bool` | `True`, `False` | Vrai ou faux ; vérifier la règle de conversion |
| `list`, `tuple` | `["ssh"]`, `("ssh",)` | Valeurs ordonnées ; indices à partir de 0 |
| `dict` | `{"nom": "srv-web"}` | Valeurs accessibles par une clé |
| `bytes`, `bytearray` | `b"SSH"`, `bytearray(b"SSH")` | Octets ; `bytearray` est modifiable |
| `None` | `None` | Absence de valeur ; ce n’est pas le texte `"None"` |

```python
charge = int("85")
texte_actif = "oui"
actif = texte_actif == "oui"
nom = " SRV-PARIS-WEB-01 ".strip().lower()
machine = {"nom": nom, "charge": charge, "actif": actif}
print(f"{machine['nom']} : {charge} %")
```

`bool("non")` vaut `True` car la chaîne n’est pas vide. Pour oui/non, valider puis comparer au texte attendu.
`=` affecte une valeur ; `==` compare. `and`, `or`, `not` combinent des conditions.

```python
charges = [42, 80, 85]
for charge in charges:
    if charge >= 80:
        print("ALERTE")
    else:
        print("OK")
```

`if/elif/else` choisit une branche. `for` parcourt des éléments. `while` répète tant que la condition est vraie :
modifier ce qui permettra de terminer, par exemple un compteur. `break` arrête la boucle ; `continue` passe au tour
suivant. Les deux-points ouvrent le bloc ; l’indentation fait partie de la syntaxe.

## 3. Réutiliser les fonctions, les collections et les objets

### Fonctions et mutabilité

```python
def est_en_alerte(pourcentage: float, seuil: int = 80) -> bool:
    return pourcentage >= seuil


print(est_en_alerte(85))
print(est_en_alerte(85, seuil=90))
```

Résultats : `True`, puis `False`. `return` fournit un résultat réutilisable ; `print` l’affiche.
Une fonction sans `return` explicite renvoie `None`. Les annotations indiquent les types attendus ; elles ne
convertissent pas les données.

Une affectation copie une **référence** : `copie = original` ne crée pas une nouvelle liste. `original.copy()` crée une
copie superficielle ; les objets imbriqués restent partagés. Listes, dictionnaires et `bytearray` sont mutables ;
chaînes, nombres, booléens, `bytes` et tuples sont immuables. Un tuple peut toutefois contenir un objet mutable.
Éviter une liste comme valeur par défaut : utiliser `None`, puis créer la liste dans la fonction.

### Générateurs et objets

```python
def charges_candidates():
    yield 42
    yield 85


flux = charges_candidates()
print(list(flux))
print(list(flux))
```

Résultats : `[42, 85]`, puis `[]`. `yield` produit à la demande. Recréer le générateur pour recommencer ; une liste
convient aux lectures répétées ou à l’accès par indice. Une IP générée est une **candidate**, pas un hôte découvert.

Une **classe** décrit un type ; une **instance** est un objet de ce type. `__init__` initialise ses attributs ; une
méthode reçoit l’instance dans `self`. Créer les listes propres à chaque instance dans `__init__`.
Un **module** est une unité importable, souvent un fichier `.py` ; une **bibliothèque** regroupe du code réutilisable.
Le bloc `if __name__ == "__main__":` évite de lancer la démonstration lors d’un import.

## 4. Lire les fichiers et traiter les erreurs

### Chemins, texte et binaire

```python
from pathlib import Path

source = Path("donnees/message.txt")
with source.open(encoding="utf-8") as fichier:
    texte = fichier.read()
octets = source.read_bytes()
print(texte.startswith("Rapport"))
print(octets == texte.encode("utf-8"))
```

Ces deux contrôles donnent `True` sur le fichier fourni. Un chemin relatif dépend du **dossier courant**.
Donner un encodage au texte ; lire le binaire comme des octets. `with` ferme le fichier, même en cas d’exception.
Le mode `w` remplace le contenu ; `a` ajoute ; `x` refuse de remplacer un fichier existant.

<a id="erreurs-et-débogage"></a>

### Exceptions et diagnostic

```python
try:
    charge = int("inconnue")
except ValueError:
    print("Charge invalide")
finally:
    print("Tentative terminée")
```

`except` traite une conversion prévue en échec ; `finally` s’exécute dans les deux cas. Éviter de masquer une erreur
inattendue sous un résultat de réussite. Une **exception** et un **code retour** sont deux notions différentes.

Pour un traceback : lire le type et le message en bas, retrouver la dernière ligne de son code, vérifier la valeur,
son type et le chemin, puis corriger une cause et relancer le même cas ainsi qu’un cas valide.

```sh
uv run python ateliers/02/debogage.py --cas type
uv run python ateliers/02/debogage.py --cas chemin
```

Ces démonstrations capturent volontairement une erreur. `--corrige` montre le comportement corrigé.
Si les imports ou le Python semblent incohérents, relancer le diagnostic et consulter le [dépannage](depannage.md).

## 5. Analyser les données et contrôler les échanges

| Besoin | Outil et geste | Preuve à relire |
| --- | --- | --- |
| Extraire un événement | `re` : motif, groupes, puis validation | Ligne acceptée ou rejetée avec son contexte |
| Passer des paramètres | `argparse` : aide, source, seuil et sortie | Arguments valides et code retour |
| Lire un export | `csv`, Pandas ; convertir et contrôler les colonnes | Types, lignes, rejets et valeurs manquantes |
| Rapprocher des tables | Pandas : clé et cardinalité de jointure | Pas de multiplication des événements |
| Conserver un rapport | SQLite : paramètres séparés du SQL, transaction | Lignes relues et sélection des alertes |
| Interroger une API | `requests` : délai, statut, JSON et champs | Réponse interprétable ou erreur conservée |
| Extraire du HTML | Scrapy : sélecteurs et valeurs absentes | Données extraites avec un statut explicite |
| Archiver et transmettre | `zipfile`/`tarfile`, `email`, `smtplib` | Membres, noms et octets reçus identiques |

**Logs :** un motif reconnu ne prouve pas une intrusion. Valider les valeurs extraites et distinguer IP source et
machine cible. Conserver les rejets et les IP inconnues. Un succès ne s’ajoute pas au compteur d’échecs.

**CSV/Excel :** `split(",")` ne remplace pas un lecteur CSV : guillemets, séparateurs et champs vides demandent un
traitement adapté. Relire les exports ; le rapport complet conserve les inconnues. Une sélection d’alertes ne le
remplace pas. Une jointure doit respecter l’unicité attendue de sa clé.

**Base :** une transaction valide un groupe d’écritures ou l’annule. Passer les valeurs dans les paramètres de
`execute`, jamais en les collant au SQL. SQLite est une base relationnelle dans un fichier, sans serveur à installer.

**Web :** HTTP 200 ne garantit ni la forme ni le sens des données. Le service de géolocalisation du cours est simulé ;
un pays fictif n’est pas la localisation réelle d’une IP. La géolocalisation reste une estimation.

**Archives et e-mail :** relire les membres et les octets. Le SMTP du cours capture localement le message ; il ne le
distribue pas à une boîte externe. L’acceptation SMTP ne prouve pas la lecture.

### Exemples de contrôle depuis le terminal

```sh
uv run python outils/analyse_logs.py --help
uv run python outils/verifier.py tp04 --etape rapport
uv run python outils/verifier.py tp05 --etape sqlite
```

Le client `analyse_logs.py` renvoie 0 si le traitement réussit, 1 en cas d’erreur de lecture/écriture et 2 pour un
argument invalide. Ces codes ne signifient pas « aucune alerte » ; leur sens dépend du programme.

## 6. Observer et administrer une seule VM

### Commandes et journaux

`subprocess.run` lance un autre programme. Fournir une liste d’arguments, un délai et lire le code retour, `stdout`
et `stderr`. Ne pas confondre une commande terminée avec une observation suffisante ; garder les erreurs visibles.

```python
import shutil

disque = shutil.disk_usage("/")
pourcentage = disque.used / disque.total * 100
print(0 <= pourcentage <= 100)
```

Cette mesure concerne le volume contenant `/`, sur la machine qui exécute Python. Les nombres varient selon le poste.
Les diagnostics de services et les commandes Linux demandent Linux ; leur résultat ne se transpose pas tel quel à macOS.
Le journal technique garde date UTC, niveau, étape, cible et erreur ; il reste distinct du rapport métier.

### SSH, Fabric et Ansible

**Une VM par personne.** La VM lance les outils (**contrôleur**) et reçoit la connexion SSH (**cible**) à
`127.0.0.1`. L’accès au bureau distant ne valide pas SSH. Le serveur SSH doit déjà être installé et démarré.

Depuis le projet **dans votre VM Linux**, préparer une fois puis contrôler :

```sh
uv run python outils/preparer_ssh_local.py
uv run python outils/diagnostic.py --distant
```

La préparation crée une clé dans `.labo/`, ajoute sa clé publique au compte Linux et prépare l’inventaire.
Elle conserve les clés existantes et refuse de remplacer un inventaire déjà présent : ne pas la relancer
systématiquement. Le diagnostic doit valider **une cible**. Voir le [guide SSH](../laboratoire/README.md).

**Fabric** pilote des commandes et transfère des fichiers par SSH/SFTP. **Ansible** décrit l’état attendu :
prévisualiser, appliquer, relire contenu et permissions, puis rejouer. `changed=0` au second passage ne remplace pas
la relecture. Une collecte partielle garde les erreurs et bloque une diffusion qui exige cette collecte.

```sh
uv run python outils/collecter_parc.py --laboratoire
uv run python outils/verifier.py tp06 --complet --laboratoire
```

Après avoir complété le TP6, le contrôle vérifie aussi `~/pyx-tp06/supervision.ini`.
Docker est une variante facultative ; aucune deuxième VM ni connexion aux autres personnes n’est demandée.

## 7. Utiliser le seuil disque : atelier 7 optionnel

L’[atelier 7](../ateliers/07/README.md) réutilise l’INI déployé au TP6, ou la copie fournie. Il dure 35 à 45 minutes,
essais et correction compris. **Une exécution produit une observation**, sans modifier la configuration.

```ini
[supervision]
cible=vm-locale
seuil_disque_pct=80
intervalle_s=60
```

`intervalle_s=60` ne programme pas une répétition. Il faudrait une boucle ou une planification pour recommencer.

| TODO dans `ateliers/07/depart.py` | Règle |
| --- | --- |
| `calculer_pourcentage` | Utilisé / total × 100, sans arrondir avant la décision |
| `choisir_statut` | `ALERTE` à partir du seuil, égalité incluse ; sinon `OK` |
| `construire_rapport` | Garder le statut et le contexte de l’observation |
| `choisir_code` | 0 pour `OK`, 1 pour `ALERTE` ; erreurs gérées à part |

| Mesure connue | Seuil | Décision | Code de ce script |
| --- | --- | --- | --- |
| 42 % | 80 % | `OK` | 0 |
| 80 % ou 85 % | 80 % | `ALERTE` | 1 |
| 85 % | 90 % | `OK` | 0 |
| Erreur ou TODO manquant | - | Contrôle non terminé | 2 |

`79.96` reste inférieur à `80`, même si un affichage arrondi semble atteindre le seuil.
Les simulations ne remplissent pas le disque. Le JSON distingue `simulation` et `reelle`, garde la machine, la date UTC,
le chemin mesuré, le seuil et la décision. Un `OK` ne prouve pas la santé de tous les services.

```sh
uv run python ateliers/07/verifier.py
uv run python ateliers/07/depart.py
```

Le vérificateur propre à cet atelier contrôle 29 cas ; `outils/verifier.py tous` reste celui du parcours principal.
Sans l’INI du TP6, ajouter `--config ateliers/07/donnees/supervision.exemple.ini` à `depart.py`.
Ajouter `--simulation ateliers/07/donnees/disque-normal.json` pour le cas fictif à 42 %.
Pour lire la référence sans remplacer votre fichier : `uv run python ateliers/07/verifier.py --corrige`.

## 8. Glossaire et récupération des travaux

<a id="glossaire"></a>

| Terme | Définition et exemple |
| --- | --- |
| **Contrôleur** | Machine qui lance les outils. Au TP6, votre VM exécute uv, Fabric et Ansible. |
| **Cible** | Machine visée par la connexion. Au TP6, cette même VM fournit ses mesures et reçoit l’INI. |
| **Module** | Unité importable, souvent un fichier `.py`. Le TP2 sépare la fonction et sa démonstration. |
| **Bibliothèque** | Code réutilisable. `ma_boite` est utilisé par deux clients au TP3. |
| **Exception** | Interruption du déroulement normal. `int("inconnue")` lève `ValueError`. |
| **Code retour** | Entier lu par le programme appelant. Son sens dépend du contrat de chaque script. |
| **Transaction** | Écritures validées ensemble ou annulées. Le TP5 protège l’import SQLite. |
| **Idempotence** | Répéter conserve l’état obtenu. Le second passage Ansible garde l’INI conforme. |
| **Journal technique** | Trace datée du traitement et de ses erreurs, par exemple `execution.log`. |
| **Rapport métier** | Données organisées pour décider, par exemple `rapport_complet.csv`. |

Une exception traitée ne détermine pas seule le code retour. Une transaction protège des écritures ; l’idempotence
concerne les effets d’une répétition. Le journal explique l’exécution ; le rapport permet d’analyser les données.

### Sauvegarder avant de quitter la VM

```sh
uv run python outils/sauvegarder.py
```

Télécharger l’archive annoncée et vérifier son ouverture sur votre ordinateur. Elle conserve vos scripts et résultats,
y compris l’atelier 7, et exclut `.venv`, les clés et l’inventaire `.labo/`. Recréer l’environnement avec uv pour
reprendre le projet ailleurs ; adapter les accès si la VM de formation n’est plus disponible.

**Avant une automatisation réelle :** choisir les entrées autorisées, le compte, les effets attendus, les délais,
les erreurs possibles et les preuves de réussite. Une commande planifiée doit aussi gérer les chemins, les sorties
et les éventuelles exécutions simultanées.

Pour poursuivre : [suivre une donnée](fil-donnee.md), [réutiliser un script](exploiter-script.md),
[dépannage](depannage.md), [sauvegarde](utilisation.md#sauvegarder) et
[auto-évaluation](auto-evaluation.md).
