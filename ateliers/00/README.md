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
```

Les premiers résultats sont volontairement incomplets. Modifiez le fichier dans l’éditeur, enregistrez-le, puis
relancez la commande dans le terminal. Ne tapez pas les commandes `uv run` dans l’interpréteur Python (`>>>`).
Les scripts manipulent des données fictives : ils n’effectuent aucune opération sur votre système.

## Votre première action

**Ouvrez `ateliers/00/01_variables.py` dans votre éditeur, puis suivez l’étape 1 ci-dessous.**
Les fichiers existent déjà : vous n’avez pas de fichier à créer et vous ne recopiez pas tout le cours.

## La méthode pour chaque étape

1. **Ouvrez le fichier indiqué** dans l’éditeur. Un `TODO` est un commentaire qui signale le travail à faire.
2. **Appliquez les modifications numérotées**, puis enregistrez avec Ctrl+S (Cmd+S sur macOS).
3. **Exécutez la première commande** dans le terminal pour voir ce que votre programme affiche.
4. **Exécutez la commande de vérification.** Passez à l’étape suivante quand elle affiche `Conforme`.

Si le contrôle affiche `À revoir`, comparez « Attendu » et « Obtenu », corrigez le fichier et relancez les commandes.
Les valeurs provisoires des fichiers de départ sont volontairement fausses : ce n’est pas un problème d’installation.
Ne modifiez pas `attendus.json`, `verifier.py` ni le dossier `corriges/` pour faire réussir les contrôles.

Les exemples de la rubrique « Comprendre » servent de modèles : **ils ne sont pas à coller dans votre fichier**.
Le corrigé est replié sous chaque étape ; ouvrez-le après un premier essai si vous bloquez.

| Étape | Sujet | Durée |
| --- | --- | --- |
| 1 | Variables et calculs | 10 min |
| 2 | Nettoyer et convertir du texte | 15 min |
| 3 | Listes et dictionnaires | 15 min |
| 4 | Prendre une décision | 20 min |
| 5 | Parcourir un petit parc | 15 min |
| 6 | Réutiliser un traitement | 15 min |

## 1. Variables et calculs — 10 min

**Objectif :** Afficher le nom, la mémoire libre et l’état d’un serveur.

**Ouvrez ce fichier :** [ateliers/00/01_variables.py](01_variables.py).

### 1A. Ce que vous devez modifier

1. Remplacez `nom = ""` par une affectation du texte `"srv-web-01"` à `nom`.
2. Remplacez le `0` de `ram_libre` par le calcul `ram_totale - ram_utilisee`.
3. Remplacez `False` par `True` dans la ligne qui définit `actif`.

**À conserver :** Gardez `ram_totale`, `ram_utilisee` et les trois lignes `print(...)` fournis.

### 1B. Exécuter votre programme

Enregistrez le fichier. Dans le terminal, à la racine du projet, lancez :

```sh
uv run python ateliers/00/01_variables.py
```

Vous devez obtenir ces lignes, dans cet ordre :

```text
srv-web-01
10
True
```

### 1C. Vérifier et passer à la suite

```sh
uv run python ateliers/00/verifier.py 1
```

**Étape terminée quand le contrôle affiche `01_variables : Conforme`.**
Avant de continuer, expliquez ce que calculent les lignes que vous avez modifiées.

### 1D. Comprendre les instructions utilisées

Une variable associe un nom à une valeur. `=` affecte une valeur ; `print()` l’affiche. Python distingue le texte
(`str`), les entiers (`int`), les nombres décimaux (`float`) et les booléens (`bool`, `True` ou `False`).
Les commentaires commencent par `#` et ne sont pas exécutés.

Exemple à lire (ne pas le copier dans votre exercice) :

```python
service = "web"
instances = 2
print(service)
print(instances * 4)
print(type(instances).__name__)  # int
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

**Objectif :** Transformer des données textuelles en un nom propre et un port numérique.

**Ouvrez ce fichier :** [ateliers/00/02_texte.py](02_texte.py).

### 2A. Ce que vous devez modifier

1. Sur la ligne `nom = ...`, appliquez `.strip().lower()` à `nom_brut`.
2. Sur la ligne `port = ...`, remplacez `0` par `int(port_brut)`.
3. Sur la ligne `message = ...`, écrivez une f-string qui assemble `nom`, le caractère `:` et `port`.

**À conserver :** Gardez les données brutes et les trois `print(...)`. La deuxième ligne affiche volontairement
`port + 1`, soit 23.

### 2B. Exécuter votre programme

Enregistrez le fichier. Dans le terminal, à la racine du projet, lancez :

```sh
uv run python ateliers/00/02_texte.py
```

Vous devez obtenir ces lignes, dans cet ordre :

```text
srv-web-01
23
srv-web-01:22
```

### 2C. Vérifier et passer à la suite

```sh
uv run python ateliers/00/verifier.py 2
```

**Étape terminée quand le contrôle affiche `02_texte : Conforme`.**
Avant de continuer, expliquez ce que calculent les lignes que vous avez modifiées.

### 2D. Comprendre les instructions utilisées

Une méthode est une opération attachée à une valeur : `texte.strip()` retire les espaces aux extrémités,
`texte.lower()` passe en minuscules. Ces méthodes produisent une nouvelle chaîne.
`int("12")` convertit du texte en entier. Une f-string insère une valeur entre accolades.

Exemple à lire (ne pas le copier dans votre exercice) :

```python
service = " SSH ".strip().lower()
port = int("22")
print(f"{service} utilise le port {port}")
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

**Objectif :** Ajouter un serveur et retrouver des informations dans deux collections.

**Ouvrez ce fichier :** [ateliers/00/03_collections.py](03_collections.py).

### 3A. Ce que vous devez modifier

1. Sous la liste `serveurs`, ajoutez une ligne `serveurs.append(...)` avec le texte `"srv-backup-01"`.
2. Remplacez la valeur de `premier` par `serveurs[0]` pour lire le premier élément.
3. Remplacez la valeur de `nom_machine` par `machine["nom"]` pour lire la clé `nom`.

**À conserver :** Gardez le dictionnaire `machine` et les trois `print(...)` fournis.

### 3B. Exécuter votre programme

Enregistrez le fichier. Dans le terminal, à la racine du projet, lancez :

```sh
uv run python ateliers/00/03_collections.py
```

Vous devez obtenir ces lignes, dans cet ordre :

```text
3
srv-web-01
srv-web-01
```

### 3C. Vérifier et passer à la suite

```sh
uv run python ateliers/00/verifier.py 3
```

**Étape terminée quand le contrôle affiche `03_collections : Conforme`.**
Avant de continuer, expliquez ce que calculent les lignes que vous avez modifiées.

### 3D. Comprendre les instructions utilisées

Une liste rassemble des valeurs dans un ordre. Son premier indice est **0**. `len(liste)` donne sa longueur
et `liste.append(valeur)` ajoute une valeur à la fin. Un dictionnaire associe des clés à des valeurs.

Exemple à lire (ne pas le copier dans votre exercice) :

```python
services = ["ssh", "web"]
print(services[0])  # ssh
machine = {"nom": "srv-test", "port": 22}
print(machine["port"])  # 22
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

**Objectif :** Calculer un état à partir de l’activité et de la charge du serveur.

**Ouvrez ce fichier :** [ateliers/00/04_conditions.py](04_conditions.py).

### 4A. Ce que vous devez modifier

1. À la place des commentaires TODO, avant `print(etat)`, écrivez un bloc `if not actif:`.
2. Dans ce bloc, avec quatre espaces, affectez `"hors ligne"` à `etat`.
3. Ajoutez `elif charge >= 80:` au même niveau que `if`, puis affectez `"alerte"` à `etat` dans son bloc.
4. Ajoutez `else:` au même niveau que `if`, puis affectez `"normal"` à `etat` dans son bloc.

**À conserver :** Gardez `actif = True`, `charge = 85` et `print(etat)` pour le premier contrôle.

### 4B. Exécuter votre programme

Enregistrez le fichier. Dans le terminal, à la racine du projet, lancez :

```sh
uv run python ateliers/00/04_conditions.py
```

Vous devez obtenir ces lignes, dans cet ordre :

```text
alerte
```

### 4C. Vérifier et passer à la suite

```sh
uv run python ateliers/00/verifier.py 4
```

**Étape terminée quand le contrôle affiche `04_conditions : Conforme`.**
Avant de continuer, expliquez ce que calculent les lignes que vous avez modifiées.

### 4D. Comprendre les instructions utilisées

`if` exécute un bloc si la condition est vraie. `elif` teste un autre cas et `else` traite les cas restants.
Les deux-points et l’indentation (quatre espaces) sont obligatoires. `==` compare ; `=` affecte.
On dispose aussi de `>=`, `<`, `!=`, `and`, `or` et `not`.

Exemple à lire (ne pas le copier dans votre exercice) :

```python
charge = 65
if charge >= 80:
    print("alerte")
else:
    print("normal")
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

**Pour vérifier les autres branches :** remplacez temporairement `actif` par `False` et exécutez le script :
le résultat doit être `hors ligne`. Essayez ensuite `actif = True` et `charge = 30` : vous devez obtenir `normal`.
Rétablissez `actif = True` et `charge = 85` avant de relancer le vérificateur.

## 5. Parcourir un petit parc — 15 min

**Objectif :** Afficher et compter uniquement les machines actives du parc.

**Ouvrez ce fichier :** [ateliers/00/05_boucles.py](05_boucles.py).

### 5A. Ce que vous devez modifier

1. Dans la boucle `for` fournie, remplacez `pass` par `if machine["actif"]:` (quatre espaces avant `if`).
2. Dans ce `if`, écrivez `print(machine["nom"])` (huit espaces avant `print`).
3. Toujours dans ce `if`, ajoutez `compteur += 1` avec la même indentation.

**À conserver :** Gardez les données, `compteur = 0` avant la boucle et le dernier `print(...)` hors de la boucle.

### 5B. Exécuter votre programme

Enregistrez le fichier. Dans le terminal, à la racine du projet, lancez :

```sh
uv run python ateliers/00/05_boucles.py
```

Vous devez obtenir ces lignes, dans cet ordre :

```text
srv-web-01
srv-backup-01
Actives : 2
```

### 5C. Vérifier et passer à la suite

```sh
uv run python ateliers/00/verifier.py 5
```

**Étape terminée quand le contrôle affiche `05_boucles : Conforme`.**
Avant de continuer, expliquez ce que calculent les lignes que vous avez modifiées.

### 5D. Comprendre les instructions utilisées

`for` parcourt chaque élément d’une collection. Une variable d’accumulation est initialisée avant la boucle.
`+= 1` augmente une valeur de un. Pour filtrer, placez un `if` dans le bloc `for`.

Exemple à lire (ne pas le copier dans votre exercice) :

```python
for service in ["ssh", "web"]:
    print(service)
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

**Objectif :** Écrire une fonction qui indique si un serveur est prioritaire.

**Ouvrez ce fichier :** [ateliers/00/06_fonctions.py](06_fonctions.py).

### 6A. Ce que vous devez modifier

1. Dans `est_prioritaire`, repérez la ligne `return False` : c’est la seule ligne de code à modifier.
2. Remplacez `False` par une expression qui combine `actif` et `charge >= 80` avec `and`.
3. Gardez `return` et les quatre espaces au début de la ligne : la fonction doit renvoyer le résultat.

**À conserver :** Gardez la définition `def ...` et les trois appels `print(est_prioritaire(...))` fournis.

### 6B. Exécuter votre programme

Enregistrez le fichier. Dans le terminal, à la racine du projet, lancez :

```sh
uv run python ateliers/00/06_fonctions.py
```

Vous devez obtenir ces lignes, dans cet ordre :

```text
True
False
False
```

### 6C. Vérifier et passer à la suite

```sh
uv run python ateliers/00/verifier.py 6
```

**Étape terminée quand le contrôle affiche `06_fonctions : Conforme`.**
Avant de continuer, expliquez ce que calculent les lignes que vous avez modifiées.

### 6D. Comprendre les instructions utilisées

`def` définit une fonction. Ses paramètres reçoivent les valeurs transmises lors de l’appel.
`return` renvoie un résultat et termine cet appel ; `print` affiche du texte mais ne remplace pas `return`.

Exemple à lire (ne pas le copier dans votre exercice) :

```python
def doubler(nombre):
    return nombre * 2


resultat = doubler(4)
print(resultat)  # 8
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
