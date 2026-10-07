# Atelier 0 — Prendre en main Python

[Retour à l’accueil](../../README.md)

**Durée indicative : 1 h 30, avec accompagnement.** Aucun prérequis Python. Si vous découvrez aussi la programmation,
prenez davantage de temps : l’objectif est de comprendre, pas de terminer à tout prix. L’installation se fait avant
ce temps de pratique, avec le [guide de démarrage](../../README.md#démarrer-sur-votre-ordinateur-personnel).
Cet atelier prépare le TP 01 ; il ne demande ni Linux, ni Docker, ni serveur SSH.

## Avant de commencer

Ouvrez la racine du projet dans votre éditeur et son terminal. Si vous avez déjà cloné le dépôt, récupérez cet atelier
avec `git pull --ff-only`. Si Git signale un conflit avec vos modifications, demandez de l’aide et conservez vos
fichiers. Avec un téléchargement ZIP, récupérez une nouvelle copie dans un autre dossier pour préserver votre travail.

```sh
uv sync --locked
uv run python ateliers/00/01_variables.py
```

Les premiers résultats sont volontairement incomplets. Modifiez le fichier dans l’éditeur, enregistrez-le, puis
relancez la commande dans le terminal. Ne tapez pas les commandes `uv run` dans l’interpréteur Python (`>>>`).
Les scripts manipulent des données fictives : ils n’effectuent aucune opération sur votre système.

## Comment avancer

Pour chaque étape : lisez l’exemple, prédisez son résultat, complétez les TODO, exécutez et vérifiez. Gardez le corrigé
fermé jusqu’à votre premier essai. Un contrôle « À revoir » est normal tant que le fichier reste à compléter.
Les contrôles comparent les affichages attendus : expliquez aussi votre code pour vérifier votre compréhension.
Les chaînes affichées, leur casse et leur ordre comptent ; retirez les affichages de débogage avant la vérification.

| Étape | Sujet | Durée |
| --- | --- | --- |
| 1 | Variables et calculs | 10 min |
| 2 | Nettoyer et convertir du texte | 15 min |
| 3 | Listes et dictionnaires | 15 min |
| 4 | Prendre une décision | 20 min |
| 5 | Parcourir un petit parc | 15 min |
| 6 | Réutiliser un traitement | 15 min |

## 1. Variables et calculs — 10 min

Une variable associe un nom à une valeur. `=` affecte une valeur ; `print()` l’affiche. Python distingue le texte
(`str`), les entiers (`int`), les nombres décimaux (`float`) et les booléens (`bool`, `True` ou `False`).
Les commentaires commencent par `#` et ne sont pas exécutés.

```python
service = "web"
instances = 2
print(service)
print(instances * 4)
print(type(instances).__name__)  # int
```

Complétez le nom du serveur, calculez la mémoire libre par soustraction et indiquez que le serveur est actif.
Ne mettez pas de guillemets autour d’un nombre ou de `True`.

**Fichier à compléter :** [01_variables.py](01_variables.py).

```sh
uv run python ateliers/00/01_variables.py
uv run python ateliers/00/verifier.py 1
```

Affichage attendu :

```text
srv-web-01
10
True
```

<details>
<summary>Voir le corrigé commenté</summary>

```python
nom = "srv-web-01"  # str : le nom est du texte.
ram_totale = 16  # int : la quantité est un nombre entier.
ram_utilisee = 6
ram_libre = ram_totale - ram_utilisee  # Calculer plutôt que recopier 10.
actif = True  # bool : pas de guillemets, majuscule obligatoire.
print(nom)
print(ram_libre)
print(actif)
```

Pour exécuter le corrigé fourni :

```sh
uv run python ateliers/00/corriges/01_variables.py
```

</details>

## 2. Nettoyer et convertir du texte — 15 min

Une méthode est une opération attachée à une valeur : `texte.strip()` retire les espaces aux extrémités,
`texte.lower()` passe en minuscules. Ces méthodes produisent une nouvelle chaîne.
`int("12")` convertit du texte en entier. Une f-string insère une valeur entre accolades.

```python
service = " SSH ".strip().lower()
port = int("22")
print(f"{service} utilise le port {port}")
```

Nettoyez le nom, convertissez le port en entier et construisez le message demandé. Comparez ensuite
`"22" + "1"` et `int("22") + 1` dans un petit fichier : concaténation et addition sont différentes.

**Fichier à compléter :** [02_texte.py](02_texte.py).

```sh
uv run python ateliers/00/02_texte.py
uv run python ateliers/00/verifier.py 2
```

Affichage attendu :

```text
srv-web-01
23
srv-web-01:22
```

<details>
<summary>Voir le corrigé commenté</summary>

```python
nom_brut = "  SRV-WEB-01  "
port_brut = "22"
nom = nom_brut.strip().lower()  # Chaque méthode renvoie une chaîne.
port = int(port_brut)  # La conversion rend possible une addition numérique.
message = f"{nom}:{port}"  # Les accolades insèrent les valeurs.
print(nom)
print(port + 1)
print(message)
```

Pour exécuter le corrigé fourni :

```sh
uv run python ateliers/00/corriges/02_texte.py
```

</details>

## 3. Listes et dictionnaires — 15 min

Une liste rassemble des valeurs dans un ordre. Son premier indice est **0**. `len(liste)` donne sa longueur
et `liste.append(valeur)` ajoute une valeur à la fin. Un dictionnaire associe des clés à des valeurs.

```python
services = ["ssh", "web"]
print(services[0])  # ssh
machine = {"nom": "srv-test", "port": 22}
print(machine["port"])  # 22
```

Ajoutez le troisième serveur à la liste et lisez le nom dans le dictionnaire. Ne confondez pas l’indice numérique
d’une liste avec la clé textuelle d’un dictionnaire. Une clé absente provoque `KeyError`.

**Fichier à compléter :** [03_collections.py](03_collections.py).

```sh
uv run python ateliers/00/03_collections.py
uv run python ateliers/00/verifier.py 3
```

Affichage attendu :

```text
3
srv-web-01
srv-web-01
```

<details>
<summary>Voir le corrigé commenté</summary>

```python
serveurs = ["srv-web-01", "srv-db-01"]
serveurs.append("srv-backup-01")  # append modifie la liste, sans la réaffecter.
machine = {"nom": "srv-web-01", "port": 22, "actif": True}
premier = serveurs[0]  # Les indices commencent à zéro.
nom_machine = machine["nom"]  # Une clé donne accès à sa valeur.
print(len(serveurs))
print(premier)
print(nom_machine)
```

Pour exécuter le corrigé fourni :

```sh
uv run python ateliers/00/corriges/03_collections.py
```

</details>

## 4. Prendre une décision — 20 min

`if` exécute un bloc si la condition est vraie. `elif` teste un autre cas et `else` traite les cas restants.
Les deux-points et l’indentation (quatre espaces) sont obligatoires. `==` compare ; `=` affecte.
On dispose aussi de `>=`, `<`, `!=`, `and`, `or` et `not`.

```python
charge = 65
if charge >= 80:
    print("alerte")
else:
    print("normal")
```

Écrivez une décision à trois branches : serveur inactif → `hors ligne` ; sinon charge au moins égale à 80 → `alerte` ;
sinon → `normal`. Essayez ensuite les trois cas en changeant les données, puis rétablissez `True` et `85`
pour le contrôle automatique.

**Fichier à compléter :** [04_conditions.py](04_conditions.py).

```sh
uv run python ateliers/00/04_conditions.py
uv run python ateliers/00/verifier.py 4
```

Affichage attendu :

```text
alerte
```

<details>
<summary>Voir le corrigé commenté</summary>

```python
actif = True
charge = 85
if not actif:  # Priorité : une machine arrêtée est hors ligne quelle que soit sa charge.
    etat = "hors ligne"
elif charge >= 80:  # Cette branche n'est testée que si la machine est active.
    etat = "alerte"
else:
    etat = "normal"
print(etat)
```

Pour exécuter le corrigé fourni :

```sh
uv run python ateliers/00/corriges/04_conditions.py
```

</details>

## 5. Parcourir un petit parc — 15 min

`for` parcourt chaque élément d’une collection. Une variable d’accumulation est initialisée avant la boucle.
`+= 1` augmente une valeur de un. Pour filtrer, placez un `if` dans le bloc `for`.

```python
for service in ["ssh", "web"]:
    print(service)
```

Parcourez les dictionnaires du parc. Affichez uniquement les noms des machines actives, puis leur nombre.
Gardez le dernier `print` après la boucle : il affiche le total une seule fois.

**Fichier à compléter :** [05_boucles.py](05_boucles.py).

```sh
uv run python ateliers/00/05_boucles.py
uv run python ateliers/00/verifier.py 5
```

Affichage attendu :

```text
srv-web-01
srv-backup-01
Actives : 2
```

<details>
<summary>Voir le corrigé commenté</summary>

```python
parc = [
    {"nom": "srv-web-01", "actif": True},
    {"nom": "srv-db-01", "actif": False},
    {"nom": "srv-backup-01", "actif": True},
]
compteur = 0  # Initialiser une seule fois, avant la boucle.
for machine in parc:
    if machine["actif"]:  # Le champ est déjà un booléen.
        print(machine["nom"])
        compteur += 1  # Compter uniquement les machines retenues.
print(f"Actives : {compteur}")  # Hors de la boucle : bilan final.
```

Pour exécuter le corrigé fourni :

```sh
uv run python ateliers/00/corriges/05_boucles.py
```

</details>

## 6. Réutiliser un traitement — 15 min

`def` définit une fonction. Ses paramètres reçoivent les valeurs transmises lors de l’appel.
`return` renvoie un résultat et termine cet appel ; `print` affiche du texte mais ne remplace pas `return`.

```python
def doubler(nombre):
    return nombre * 2


resultat = doubler(4)
print(resultat)  # 8
```

Complétez `est_prioritaire` : une machine est prioritaire si elle est active **et** si sa charge atteint 80.
Renvoyez un booléen. Les trois appels vérifient une machine chargée, une machine arrêtée et une machine peu chargée.
Pour finir, expliquez oralement le rôle de chaque ligne avant d’ouvrir le corrigé.

**Fichier à compléter :** [06_fonctions.py](06_fonctions.py).

```sh
uv run python ateliers/00/06_fonctions.py
uv run python ateliers/00/verifier.py 6
```

Affichage attendu :

```text
True
False
False
```

<details>
<summary>Voir le corrigé commenté</summary>

```python
def est_prioritaire(actif: bool, charge: int) -> bool:
    # and exige que les deux conditions soient vraies.
    # return permet au code appelant de réutiliser le résultat.
    return actif and charge >= 80


print(est_prioritaire(True, 90))  # Active et chargée : True.
print(est_prioritaire(False, 90))  # Inactive : False, même si la charge est élevée.
print(est_prioritaire(True, 30))  # Active mais peu chargée : False.
```

Pour exécuter le corrigé fourni :

```sh
uv run python ateliers/00/corriges/06_fonctions.py
```

</details>

## Vérifier l’ensemble et passer au TP 01

```sh
uv run python ateliers/00/verifier.py
```

Vous êtes prêt à commencer le [TP 01](../01/README.md) si vous savez :

- Créer une variable et distinguer `"22"` de `22`.
- Lire une valeur dans une liste et un dictionnaire.
- Écrire une condition et indenter son bloc.
- Parcourir des machines et compter celles qui respectent une condition.
- Écrire une fonction qui renvoie un résultat.

Si une étape bloque, reprenez son exemple et demandez une explication avant de poursuivre.
Les boucles `while`, les exceptions, les fichiers et les autres collections seront approfondis dans les TP suivants.

## Comprendre les erreurs courantes

| Message | Première vérification |
| --- | --- |
| `SyntaxError` | Guillemets, parenthèses et deux-points après `if`, `for` ou `def`. |
| `IndentationError` | Quatre espaces par niveau, sans mélange de tabulations. |
| `NameError` | Variable définie avant usage, orthographe et majuscules. |
| `TypeError` | Texte et nombre mélangés ; conversion avec `int` si nécessaire. |
| `KeyError` | Clé présente et correctement écrite dans le dictionnaire. |

Lisez la dernière ligne de l’erreur puis le numéro de ligne indiqué. Une erreur pendant l’apprentissage est normale.
Pour vérifier seulement les corrigés fournis : `uv run python ateliers/00/verifier.py --corrige`.
