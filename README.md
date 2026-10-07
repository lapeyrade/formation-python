# Python pour l’administration système

Automatisez une intervention sur un parc : inventaire, adressage, diagnostic Linux, analyse d’incidents et collecte SSH.
Vous débutez en Python ? Commencez par l’[atelier 0 : les bases de Python](ateliers/00/README.md), guidé sur 1 h 30.
Six TP d’administration système prolongent cette introduction avec leurs données, aides, corrigés et contrôles.

## Récupérer le projet

Avec Git, ouvrez un terminal dans votre dossier de travail et lancez :

```sh
git clone https://github.com/lapeyrade/formation-python.git
cd formation-python
```

Sans Git, utilisez **Code > Download ZIP** sur la page du dépôt GitHub, puis décompressez le fichier téléchargé.
Le dossier obtenu s’appelle généralement `formation-python-main`. Ouvrez ce dossier complet dans votre éditeur.

Dans les deux cas, la racine du projet est le dossier contenant `README.md`, `pyproject.toml` et `uv.lock`.
Toutes les commandes des TP se lancent depuis cette racine. Choisissez ensuite la procédure adaptée à votre poste.

## Commencer dans le poste Linux

Connectez-vous au poste de formation, récupérez le projet complet et ouvrez-le dans VS Code. Le code et les commandes
s’exécutent dans ce poste. Suivez le [guide d’installation](docs/installation.md), puis lancez depuis le dossier
contenant ce README et pyproject.toml :

```sh
uv sync --locked
uv run python outils/diagnostic.py
uv run python ateliers/01/depart.py
```

Le diagnostic doit confirmer Python, les imports, les données, l’écriture et Ansible natif. Les accès SSH se contrôlent
séparément avant le TP 06. Ouvrez ensuite le [TP 01](ateliers/01/README.md).

## Démarrer sur votre ordinateur personnel

Cette procédure permet de commencer le **TP 01 en local**, en attendant un poste Linux. Le parc et les connexions de
ce TP sont simulés : aucune cible SSH ni installation Docker n’est nécessaire pour cette première demi-journée.
Le démarrage ci-dessous doit être vérifié sur votre poste ; le parcours complet n’est pas validé en Windows natif.

### 1. Installer un éditeur

Installez [Visual Studio Code](https://code.visualstudio.com/download), puis l’extension **Python** publiée par
**Microsoft** depuis son panneau Extensions. Un éditeur Python déjà installé convient aussi.

### 2. Installer uv

uv gère Python et les bibliothèques du projet. Il n’est pas nécessaire d’installer Python ou Anaconda séparément.
Si `uv --version` affiche déjà une version, passez à l’étape suivante.

**Windows :** ouvrez **PowerShell** et exécutez l’installateur officiel :

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS ou Linux :** ouvrez **Terminal** et exécutez :

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Fermez puis rouvrez le terminal et VS Code pour prendre en compte le chemin de uv. Vérifiez :

```sh
uv --version
```

Ces commandes téléchargent et exécutent l’installateur de l’éditeur. Autres méthodes et détails :
[documentation officielle de uv](https://docs.astral.sh/uv/getting-started/installation/).
Si votre poste professionnel bloque l’installation ou les téléchargements, signalez le message au formateur.

### 3. Ouvrir le projet complet

Récupérez le projet comme indiqué [plus haut](#récupérer-le-projet), dans un dossier de votre compte utilisateur.
Dans VS Code, utilisez **Fichier > Ouvrir le dossier** et sélectionnez la racine du projet, qui contient
`pyproject.toml`, `uv.lock`,
`ateliers/`, `donnees/`, `src/` et `outils/`. N’ouvrez pas seulement le fichier `depart.py`.

Ouvrez **Terminal > Nouveau terminal**. Sous Windows, utilisez PowerShell ; sous macOS ou Linux, le terminal habituel.
Vérifiez que vous êtes à la racine du projet :

```sh
uv --version
ls pyproject.toml uv.lock
```

### 4. Préparer Python et les bibliothèques

Les commandes suivantes sont identiques dans PowerShell, macOS et Linux :

```sh
uv sync --locked
uv run python --version
uv run python outils/bienvenue.py
```

uv utilise la version Python 3.13 fixée dans `.python-version`, la télécharge si nécessaire et crée `.venv`.
La synchronisation installe les dépendances du projet complet, y compris celles des prochains TP : le premier
lancement demande Internet et peut prendre quelques minutes. Le message de bienvenue affiche le poste et le système
réellement utilisés. Sur Windows natif, le projet exclut Ansible de l’installation.

### 5. Sélectionner Python dans VS Code

Ouvrez la palette avec **Ctrl+Maj+P** sur Windows/Linux ou **Cmd+Maj+P** sur macOS, puis choisissez
**Python: Select Interpreter**. Sélectionnez l’interpréteur de ce projet :

| Système | Interpréteur |
| --- | --- |
| Windows natif | `.venv\Scripts\python.exe` |
| macOS / Linux | `.venv/bin/python` |

S’il n’apparaît pas, utilisez **Enter interpreter path** pour le sélectionner. Dans le terminal, gardez les commandes
`uv run` des énoncés : elles utilisent l’environnement du projet sans activation manuelle.
Voir la [documentation des environnements VS Code](https://code.visualstudio.com/docs/python/environments).

### 6. Commencer et vérifier le TP 01

Ouvrez `ateliers/01/depart.py`, puis exécutez :

```sh
uv run python ateliers/01/depart.py
```

Les messages « À compléter » sont attendus. Complétez les TODO de la première étape, enregistrez le fichier, puis
contrôlez les résultats :

```sh
uv run python outils/verifier.py tp01 --etape types
```

« À revoir » ou un code de sortie 1 indique que les résultats ne correspondent pas encore aux critères. Après
correction, le contrôle doit annoncer « Conforme ». Poursuivez avec les étapes `boucles`, puis `masques`, en suivant
[l’énoncé du TP 01](ateliers/01/README.md). Les productions se trouvent dans `sorties/`.

Dans ce TP, `pwd` et `hostname` servent seulement à identifier le contexte ; ils sont aussi disponibles dans
PowerShell. Le nom et les chemins affichés sont ceux de votre ordinateur, pas ceux d’un poste Linux distant.

### Limites du travail local et suite du parcours

| Partie | Windows natif / macOS |
| --- | --- |
| TP 01 : types, boucles, texte et masques | Mécanismes Python portables ; commencer avec les commandes ci-dessus. |
| Fichiers, CSV/Excel, SQLite, API et archives | Bibliothèques disponibles, mais tous les scripts du parcours ne sont pas validés sur Windows. |
| Diagnostic Linux du TP 03 | Nécessite Linux pour observer `/proc`, les routes avec `ip` et les unités `systemd`. |
| Contrôleur Ansible du TP 06 | Windows natif non pris en charge ; macOS peut être contrôleur, avec deux cibles Linux accessibles. |

Le diagnostic global `outils/diagnostic.py` vérifie le contexte prévu pour toute la formation, dont Ansible :
il ne constitue pas le test de démarrage du TP 01 sous Windows. Les observations Linux peuvent être signalées comme
non applicables sur un autre système ; cela ne signifie pas que leurs objectifs pédagogiques sont réalisés.

Pour poursuivre le parcours complet, privilégiez le poste Linux de formation. Une VM Linux, ou WSL2 sous Windows,
peut servir de secours après préparation et vérification avec le formateur ; WSL2 ne garantit pas à lui seul la
présence de systemd ni les accès aux deux cibles. Ansible précise que WSL n’est pas un contrôleur officiellement
pris en charge pour la production : voir les
[limites Windows d’Ansible](https://docs.ansible.com/projects/ansible/latest/os_guide/intro_windows.html).

Lors du passage au poste Linux, transférez vos fichiers de travail et recréez l’environnement avec `uv sync --locked`.
Ne transférez pas `.venv` d’un système à l’autre. Les cibles SSH se préparent séparément avant le TP 06.

### Si une commande bloque

- **uv introuvable :** rouvrez entièrement le terminal et VS Code après installation.
- **pyproject.toml introuvable :** ouvrez la racine du projet, pas son parent ni `ateliers/01` seul.
- **Import introuvable :** relancez `uv sync --locked`, puis utilisez `uv run python`, pas un Python système différent.
- **Téléchargement refusé :** transmettez le message au formateur pour vérifier le proxy ou les restrictions du poste.

## Le parcours

| TP | Objectif |
| --- | --- |
| 00 | [Prendre en main Python : variables, collections, conditions, boucles et fonctions](ateliers/00/README.md) |
| 01 | [Qualifier un parc et préparer ses réseaux](ateliers/01/README.md) |
| 02 | [Fiabiliser un import et réutiliser son code](ateliers/02/README.md) |
| 03 | [Préparer un adressage et diagnostiquer un hôte](ateliers/03/README.md) |
| 04 | [Analyser un incident SSH et Web](ateliers/04/README.md) |
| 05 | [Enrichir et conserver les rapports du SI](ateliers/05/README.md) |
| 06 | [Collecter à distance et diffuser les alertes](ateliers/06/README.md) |

Chaque TP peut repartir de ses données fournies. Complétez les fichiers de l’énoncé, puis vérifiez vos résultats. Les
messages « À compléter » sont normaux au premier lancement ; les indices sont dépliables.

Les schémas des énoncés situent les entrées, les traitements et les sorties avant la lecture du code. Les guides
d’installation et de connexion illustrent aussi les rôles du poste de travail et des cibles SSH.

- [Installer et vérifier le projet](docs/installation.md)
- [Se repérer dans Linux](docs/linux.md)
- [Exécuter, contrôler et retrouver les résultats](docs/utilisation.md)
- [Configurer les deux cibles SSH](laboratoire/README.md)
- [Mémo Python et uv, avec glossaire](docs/memo-python-uv.md)
- [Suivre une donnée jusqu’au message](docs/fil-donnee.md)
- [Réutiliser un script après le cours](docs/exploiter-script.md)
- [Dépannage](docs/depannage.md)
- [Auto-évaluation](docs/auto-evaluation.md) et [questionnaires de progression](docs/questionnaires.md)

Python et Ansible sont gérés avec uv. Les services HTTP et SMTP de test tournent dans le poste Linux ; un appel public
guidé complète la géolocalisation du TP 05 ; les e-mails sont capturés localement. Docker est seulement une solution de
secours pour fournir deux cibles SSH.

## Récupérer votre travail

Avant de fermer le poste distant :

```sh
uv run python outils/sauvegarder.py
```

Le script affiche l’archive à télécharger sur votre ordinateur. Elle contient le projet modifié et les résultats, en
excluant l’environnement, les caches et les clés SSH. Voir la
[procédure de sauvegarde](docs/utilisation.md#sauvegarder).

Les [variantes de transfert](donnees/transfert/README.md) sont incluses dans les questions des TP. Elles vérifient le
raisonnement : observation, conclusion, prochaine action. Les journaux execution.log conservent le déroulement technique
de chaque essai ; ils restent distincts des rapports métier.
