# Auto-évaluation

[Accueil](../README.md) —
[Questionnaires avant/après et quotidiens](questionnaires.md)

Répondre d’abord, puis cliquer sur « Afficher la réponse commentée » sous la question. Les réponses sont fermées par
défaut.

Ouvrir ce document dans la prévisualisation Markdown de l’éditeur ou sur GitHub pour cliquer sur les corrections.

## Avant de commencer

**1. Décrire un algorithme qui filtre les hôtes actifs puis compte les hôtes par site.**

<details>
<summary>Afficher la réponse commentée</summary>

Parcourir la collection, tester actif, incrémenter le compteur du site. Ces mécanismes sont des prérequis ; le cours
travaille leur expression en Python.

</details>

**2. Comment éviter une boucle de reconnexion infinie ?**

<details>
<summary>Afficher la réponse commentée</summary>

Borner les essais, incrémenter à chaque tentative et définir la condition de sortie.

</details>

## Fin du jour 1

**1. Pourquoi bool("non") ne valide-t-il pas un champ actif ?**

<details>
<summary>Afficher la réponse commentée</summary>

Toute chaîne non vide est vraie. Normaliser puis accepter explicitement oui/non ; rejeter les autres valeurs.

</details>

**2. Pourquoi utiliser csv plutôt que split(";") ?**

<details>
<summary>Afficher la réponse commentée</summary>

CSV gère les champs cités, séparateurs et retours à la ligne dans un champ.

</details>

**3. Comment éviter de modifier le parc original via une copie ?**

<details>
<summary>Afficher la réponse commentée</summary>

Une affectation partage la référence. Copier chaque niveau effectivement modifié ou construire un nouveau résultat.

</details>

**4. Que conserver pour une ligne invalide ?**

<details>
<summary>Afficher la réponse commentée</summary>

Numéro de ligne, cause et contexte utile ; continuer les autres lignes si le contrat le permet.

</details>

**5. Pourquoi protéger le lancement d’un module ?**

<details>
<summary>Afficher la réponse commentée</summary>

Le garde `__main__` permet d’importer ses fonctions sans déclencher l’intervention.

</details>

## Fin du jour 2

**1. Une adresse produite par le générateur est-elle libre sur le réseau ?**

<details>
<summary>Afficher la réponse commentée</summary>

Non : c’est une candidate conforme aux exclusions déclarées, pas une réservation ni une preuve d’absence de conflit.

</details>

**2. Comment identifier le poste réellement mesuré et rendre son diagnostic exploitable ?**

<details>
<summary>Afficher la réponse commentée</summary>

Conserver date UTC, utilisateur, hostname, OS et chemin du volume. Pour chaque commande, garder statut, code retour,
sortie standard et erreur ; distinguer absence, échec et délai dépassé. Les valeurs observées varient selon le poste et
la date.

</details>

**3. Quel hôte représente l’IP après from dans un log SSH ?**

<details>
<summary>Afficher la réponse commentée</summary>

La source de la connexion. Le nom avant sshd identifie la cible.

</details>

**4. Pourquoi conserver les sources inconnues lors de la jointure ?**

<details>
<summary>Afficher la réponse commentée</summary>

Une jointure interne les supprimerait, masquant potentiellement des événements importants.

</details>

**5. Pourquoi un seuil d’alerte ne suffit-il pas à prouver une intrusion ?**

<details>
<summary>Afficher la réponse commentée</summary>

Il sélectionne des événements à investiguer ; il faut le contexte, la période et d’autres indices.

</details>

## Fin du jour 3

**1. Comment éviter une insertion partielle d’un rapport ?**

<details>
<summary>Afficher la réponse commentée</summary>

Valider puis insérer dans une transaction ; annuler en cas d’échec et définir la politique de doublons.

</details>

**2. Que vérifier lors d’un appel HTTP, et que désigne localhost dans le bureau distant ?**

<details>
<summary>Afficher la réponse commentée</summary>

Délai, statut, format et champs attendus. localhost désigne le poste Linux qui exécute le script. Une réponse reçue ne
garantit pas une donnée valide.

</details>

**3. Que devient la diffusion finale si une cible SSH demandée est indisponible ?**

<details>
<summary>Afficher la réponse commentée</summary>

Conserver le statut d’erreur et les observations des cibles accessibles. Le scénario refuse de diffuser ce rapport
partiel ; rétablir une collecte complète. Sans collecte demandée, la portée reste explicitement locale.

</details>

**4. Que démontre le second passage Ansible sans changement ?**

<details>
<summary>Afficher la réponse commentée</summary>

L’état demandé est déjà satisfait dans ce scénario ; cela ne prouve pas l’idempotence de toutes les tâches possibles.

</details>

**5. Quand annoncer le succès de la chaîne ?**

<details>
<summary>Afficher la réponse commentée</summary>

Après validation des résultats attendus, archivage contrôlé et acceptation par le serveur SMTP de test ; cela ne
garantit pas une livraison externe.

</details>

Avant de fermer le poste distant, expliquer comment récupérer ses scripts et résultats sans emporter les clés SSH.

<details>
<summary>Afficher la réponse commentée</summary>

exécuter `uv run python outils/sauvegarder.py`, télécharger le ZIP sur son ordinateur, puis vérifier son ouverture. Les
scripts et résultats sont conservés ; `.labo`, les clés et les configurations de connexion restent exclus. Recréer un
environnement uv lors de la reprise.

</details>
