# Lire le code des ateliers

[Retour au parcours](../README.md)

## Votre travail en quatre étapes

1. Ouvrir le README de l’atelier et la section demandée.
2. Ouvrir le fichier indiqué ; chercher le commentaire `TODO` correspondant.
3. Modifier seulement ce morceau, enregistrer, puis lancer la commande de l’énoncé dans le terminal.
4. Comparer le résultat avec l’exemple. `À revoir` signifie qu’une partie reste à corriger ; `Conforme` valide l’étape.

Un commentaire commence par `#` : Python ne l’exécute pas. Le mot TODO signifie « à faire ».
Les exemples du cours servent à comprendre : ne les collez pas tous dans votre fichier.

## Reconnaître ce qui est fourni

| Élément rencontré | À quoi il sert | Ce que vous devez faire |
| --- | --- | --- |
| `TODO` dans le fichier indiqué | Partie à compléter | Suivre la consigne de l’étape |
| `resultat` et `terminer(...)` | Préparer le bilan de vérification | Garder le code fourni, sauf TODO explicite |
| `dossier_tp(...)`, `preparer_etape(...)` | Ranger les résultats dans `sorties/` | Utiliser sans réécrire |
| `from admin_tools...` | Charger les aides propres à ce cours | Ne pas modifier `src/admin_tools/` |
| `import csv`, `from pathlib import Path` | Utiliser des outils inclus avec Python | Lire leur rôle dans le cours |
| `import pandas`, `from fabric import Connection` | Utiliser une bibliothèque installée par uv | Comprendre l’opération enseignée |
| `outils/verifier.py` | Exécuter et comparer les résultats | Le lancer sans le modifier |

Les aides du cours ne sont pas des fonctions standard de Python. Leur code reste disponible pour une lecture ultérieure.

## Lire une expression sans se perdre

Avant de lire le programme, nommez **l’entrée** et **le résultat recherché**. Décomposez ensuite les étapes sur papier :

```python
texte = " 85% "
nettoye = texte.strip()  # "85%"
sans_unite = nettoye.rstrip("%")  # "85"
pourcentage = int(sans_unite)  # 85, un nombre
print(pourcentage)
```

`strip` retire les espaces aux extrémités ; `rstrip("%")` retire le signe final ; `int` convertit en entier. Les noms
intermédiaires permettent de voir la transformation. Vous pouvez afficher une valeur avec `print` pour comprendre.

## Demander de l’aide efficacement

Indiquez l’atelier, l’étape, le fichier modifié, la commande et le message obtenu. Gardez votre essai : il permet de
comprendre le blocage. Les corrigés servent à comparer après un premier essai, puis à expliquer une différence.

Les pages « Référence facultative » des slides proposent des variantes. Elles ne sont pas des prérequis cachés aux TP.
Les durées sont indicatives : avancez avec accompagnement et privilégiez l’explication d’un résultat à la vitesse.
