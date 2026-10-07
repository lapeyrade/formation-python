# Utiliser les TP

[Retour à l’accueil](../README.md)

## Quels fichiers modifier ?

Dans chaque dossier, `README.md` donne la mission et les critères de réussite. Modifiez les blocs à compléter dans
`depart.py`. Les consignes détaillées et les indices dépliables figurent dans ce même énoncé.

Cinq TP ont des fichiers complémentaires :

- TP 02 : `inventaire_module.py`, pour distinguer import et exécution.
- TP 03 : `ma_boite/reseau.py`, `ma_boite/modeles.py`, puis les clients `generer.py` et `resumer.py`.
- TP 04 : `cli.py`, pour les paramètres de la ligne de commande.
- TP 05 : `spider.py`, pour extraire les champs d’état et de contexte de la page HTML.
- TP 06 : `distant.py`, exemple fonctionnel à adapter pour la partie SSH/Ansible, et `mes_fonctions.py` pour réutiliser
  vos fonctions validées.

Les appels `dossier_tp`, `preparer_etape` et `terminer` sont fournis pour ranger les résultats. Conservez-les. Les
fonctions de `admin_tools.pilotes` préparent aussi les essais uv, les clients, les arguments et la collecte HTML :
complétez les fichiers indiqués dans l’énoncé, sans réécrire ces pilotes. Ne modifiez pas `uv.lock`, `catalogue.json` ou
les données de référence pour faire réussir une vérification.

## Exécuter et vérifier

Depuis le dossier contenant `pyproject.toml`, exemple pour le TP 02 :

```sh
uv run python ateliers/02/depart.py
uv run python outils/verifier.py tp02
```

Le vérificateur relance votre script dans un nouvel essai. Il contrôle le livrable principal. Pour contrôler aussi les
étapes intermédiaires :

```sh
uv run python outils/verifier.py tp02 --complet
```

Un résultat `À revoir` n’efface rien : lisez le nom de l’étape, comparez la valeur attendue et la valeur obtenue, puis
corrigez votre programme. `--complet` peut encore signaler des étapes incomplètes même si le livrable principal est
correct.

## Avancer étape par étape

Pour exécuter et contrôler uniquement les boucles du TP 01 :

```sh
uv run python outils/verifier.py tp01 --etape boucles
```

Seuls le préambule (imports et préparation commune) et le bloc choisi sont exécutés. Les autres blocs peuvent rester
incomplets. Gardez les repères `# === …` fournis dans les scripts et placez les fonctions propres à une étape dans son
bloc. Une erreur dans les imports communs reste à corriger.

Chaque section de l’énoncé donne sa commande. Ajoutez `--corrige` pour essayer la même étape du corrigé. `--etape` ne se
combine ni avec `tous` ni avec `--complet`. L’étape `distant` demande aussi `--laboratoire`.

Les messages présentent chaque champ incorrect avec sa valeur attendue et sa valeur obtenue. Une réussite sur une étape
ne valide pas tout le TP : terminez par le contrôle `--complet`.

## Retrouver vos résultats

Chaque lancement indique le chemin d’un dossier tel que `sorties/tp02/essai-…`. Il contient un sous-dossier par étape et
un `bilan.json` commun. Le bilan résume les calculs ; certains contrôles relisent aussi les fichiers réellement
produits.

Un nouveau lancement crée un autre essai. Vos tentatives précédentes restent disponibles dans le poste Linux. Les
fichiers de `sorties/` et l’environnement `.venv/` sont exclus de Git.

## Utiliser les corrections

Chaque étape propose deux indices dépliables, fermés au départ. **Indice 1 - Piste conceptuelle** aide à choisir le
raisonnement. **Indice 2 - Pseudo-code** décrit les opérations à traduire en Python et rappelle le code fourni. Essayez
la première piste avant d’ouvrir la seconde ; le pseudo-code n’est pas un script à exécuter.

Vous pouvez ensuite lire `corrige.py`, comparer une étape et expliquer ce qui change dans votre version. Les critères et
les réponses aux questions restent dans leurs volets séparés.

```sh
uv run python ateliers/02/corrige.py
uv run python outils/verifier.py tp02 --corrige --complet
```

Le corrigé ne remplace pas votre fichier de départ. Au TP 03, `solution/ma_boite` et ses clients constituent une copie
complète séparée de votre package. Les fonctions de `src/admin_tools/` sont des références communes et peuvent être lues
pour comprendre les corrections.

## La partie distante du TP 06

Suivez d’abord le [guide du laboratoire](../laboratoire/README.md), puis :

```sh
uv run python ateliers/06/depart.py --laboratoire
uv run python outils/verifier.py tp06 --complet --laboratoire
```

Sans `--laboratoire`, la partie locale reste utilisable ; la collecte distante est annoncée comme non exécutée. L’option
demande réellement des connexions aux deux cibles de l’inventaire et deux passages Ansible natifs. Les cibles peuvent
être des postes Linux fournis ou les deux conteneurs de secours ; leurs noms, ports et utilisateurs sont configurables.

## Réutiliser vos rapports

Le TP 06 accepte `--source` pour choisir votre rapport du TP 04 et `--collecte` pour joindre une collecte SSH complète
déjà produite. Avec `--laboratoire`, la collecte du même essai est jointe automatiquement. Sans collecte, le diagnostic
annonce `non_executee`.

Le scénario autonome expose les mêmes entrées :

```sh
uv run python outils/rapport_final.py donnees/rapport_complet.csv --sortie sorties/rapport-final
```

La destination doit être neuve ; choisissez un autre nom pour un nouvel essai. Ajoutez `--collecte CHEMIN_COLLECTE.csv`
pour joindre votre collecte. Une collecte absente ou partielle bloque la diffusion ; aucune clé SSH n’entre dans
l’archive.

<a id="sauvegarder"></a>

## Sauvegarder avant de quitter le poste

```sh
uv run python outils/sauvegarder.py
```

Le script affiche une archive datée dans `sorties/`. Téléchargez-la sur votre ordinateur avec le mécanisme de transfert
du poste distant et vérifiez que le fichier a bien été reçu. L’archive contient vos scripts modifiés et vos résultats ;
elle exclut `.venv`, `.labo`, les caches et l’inventaire Ansible généré. Les productions du cours ne sont pas
automatiquement publiées sur GitHub.

## Faire le point

Utilisez l’[auto-évaluation](auto-evaluation.md) pour vérifier que vous savez expliquer vos résultats. Comprendre
pourquoi une correction fonctionne est aussi important que voir `Conforme` dans le terminal.

## Repères pour aller plus loin

Le [mémo Python et uv](memo-python-uv.md) rassemble les gestes fréquents. [Suivre une donnée](fil-donnee.md) relie les
fichiers des trois derniers TP. [Réutiliser un script](exploiter-script.md) montre les chemins explicites, les codes
retour et les effets d’une répétition.
