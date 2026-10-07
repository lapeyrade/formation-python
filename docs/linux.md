# Se repérer dans le poste Linux

[Retour à l’accueil](../README.md)

| Commande | Question |
| --- | --- |
| hostname | Sur quel poste le terminal s’exécute-t-il ? |
| id | Quel compte et quels groupes exécutent la commande ? |
| pwd | Quel est le dossier courant ? |
| ls | Quels fichiers contient ce dossier ? |
| df -Pk . | Quel volume contient le dossier courant et quelle place reste-t-il ? |

Les commandes des TP se lancent dans le dossier contenant pyproject.toml. Un chemin relatif part du dossier courant ; un
chemin absolu commence par /. Vos fichiers se trouvent dans le compte Linux de formation.

## Interpréter les observations

Les données du parc représentent un exemple. Le nom du poste, l’utilisateur, la date et l’espace disque mesurés sont
réels. Un chemin peut se trouver dans un volume monté : df ne décrit pas nécessairement tout le stockage physique de la
machine.

Un fichier absent, un refus de lecture et une donnée invalide sont trois situations différentes. Travaillez dans votre
dossier utilisateur. Le cours garde des données de référence pour reproduire les résultats, même si le journal système
est vide ou inaccessible.

## Lire un journal disponible

Sur Linux, le journal d’un service peut être dans un fichier ou dans le journal système. Si les droits le permettent et
si le service existe, une observation limitée peut utiliser :

```sh
journalctl -u ssh --since today --no-pager -n 10
```

Cette observation sert à reconnaître source, service, date et format. Elle n’entre pas dans le contrôle déterministe du
TP 04. Aucun événement trouvé n’indique pas à lui seul que le script est incorrect. Les fichiers auth.log et access.log
du kit restent les références du TP.

## Comprendre localhost

Lorsque client et serveur tournent dans le poste Linux, 127.0.0.1 désigne ce poste. Depuis le navigateur de votre
ordinateur personnel, 127.0.0.1 désigne votre ordinateur personnel. Les clients requests, Scrapy et SMTP fournis
s’exécutent avec leur serveur de test dans le même poste Linux.

## Avant de quitter le poste

Lancez outils/sauvegarder.py et téléchargez l’archive affichée sur votre ordinateur. Les fichiers laissés dans le poste
distant ne constituent pas une sauvegarde que vous pourrez nécessairement récupérer après la session.
