# Questionnaires de progression

[Accueil](../README.md) — [Questions ouvertes](auto-evaluation.md)

Une seule réponse par question. Choisir A, B ou C ; si vous ne savez pas encore, inscrire « ? ». Conserver vos réponses
dans deux colonnes Avant/Après, sur papier ou dans un fichier personnel.

Le positionnement reprend les mêmes dix questions avant le cours et au bilan final : il mesure une progression, sans
exiger de connaître Python à l’entrée. Les deux questions algorithmiques de l’auto-évaluation vérifient les prérequis.
Répondre avant de consulter la correction. Sous chaque question, cliquer sur « Afficher la réponse et l’explication »
pour ouvrir le corrigé ; il est fermé par défaut.

Les questionnaires de fin de journée complètent les contrôles des TP et les questions de transfert. Ils ne prouvent pas
seuls une autonomie en administration système.

Ouvrir ce document dans la prévisualisation Markdown de l’éditeur ou sur GitHub pour cliquer sur les corrections.

## Positionnement avant et après — 5 min par passage

**Q01 — Le champ actif contient le texte « non ». Comment obtenir un booléen valide ?**

- A. Appeler bool sur le texte.
- B. Normaliser puis comparer aux valeurs autorisées.
- C. Supprimer le champ.

<details>
<summary>Afficher la réponse et l’explication</summary>

**Réponse B.** Normaliser puis comparer aux valeurs autorisées.

Toute chaîne non vide est vraie ; comparer oui/non et rejeter les autres valeurs.

</details>

**Q02 — Que faut-il à une boucle de reconnexion pour terminer même sans succès ?**

- A. Un compteur borné et une condition de sortie.
- B. Une liste de messages.
- C. Un nom de fonction.

<details>
<summary>Afficher la réponse et l’explication</summary>

**Réponse A.** Un compteur borné et une condition de sortie.

Une borne et la progression du compteur empêchent une boucle infinie.

</details>

**Q03 — Une règle de seuil doit servir à deux scripts. Où placer sa logique ?**

- A. Dans deux copies indépendantes.
- B. Dans un fichier de résultats.
- C. Dans une fonction du module partagé, importée par les clients.

<details>
<summary>Afficher la réponse et l’explication</summary>

**Réponse C.** Dans une fonction du module partagé, importée par les clients.

Un contrat partagé évite des corrections divergentes ; la présentation reste dans les clients.

</details>

**Q04 — Après b = a, où a est une liste, que fait b.append("https") ?**

- A. Modifie aussi la liste accessible par a.
- B. Crée une liste indépendante.
- C. Modifie seulement le nom b.

<details>
<summary>Afficher la réponse et l’explication</summary>

**Réponse A.** Modifie aussi la liste accessible par a.

Les deux noms désignent le même objet ; une copie doit être demandée explicitement.

</details>

**Q05 — Quel rôle joue uv sync --locked dans le projet du cours ?**

- A. Change les bibliothèques du Python système.
- B. Installe le projet et ses dépendances dans son environnement à partir du verrou.
- C. Crée un rapport CSV.

<details>
<summary>Afficher la réponse et l’explication</summary>

**Réponse B.** Installe le projet et ses dépendances dans son environnement à partir du verrou.

Le Python et les bibliothèques du projet restent isolés ; uv add déclare et installe une nouvelle dépendance.

</details>

**Q06 — On parcourt un générateur jusqu’au bout. Que donne un second parcours ?**

- A. Les mêmes résultats automatiquement.
- B. Une erreur obligatoire.
- C. Aucun résultat ; il faut recréer le générateur ou mémoriser les valeurs.

<details>
<summary>Afficher la réponse et l’explication</summary>

**Réponse C.** Aucun résultat ; il faut recréer le générateur ou mémoriser les valeurs.

Un générateur conserve sa position et peut être épuisé.

</details>

**Q07 — Dans Machine("srv-web"), que représentent Machine et l’objet créé ?**

- A. Machine est la classe, l’objet est une instance avec ses attributs.
- B. Deux fichiers de configuration.
- C. Une bibliothèque externe et son verrou.

<details>
<summary>Afficher la réponse et l’explication</summary>

**Réponse A.** Machine est la classe, l’objet est une instance avec ses attributs.

La classe définit le type ; chaque instance porte son propre état et expose les méthodes prévues.

</details>

**Q08 — Quelle combinaison permet de conserver un rapport CSV dans une base sans insertion partielle ?**

- A. Concaténer des valeurs dans le SQL.
- B. Ouvrir une transaction et passer les valeurs comme paramètres SQL.
- C. Ignorer chaque erreur sans la signaler.

<details>
<summary>Afficher la réponse et l’explication</summary>

**Réponse B.** Ouvrir une transaction et passer les valeurs comme paramètres SQL.

La transaction permet l’annulation de l’ensemble ; les paramètres séparent SQL et valeurs.

</details>

**Q09 — Après un appel HTTP, quels contrôles faut-il distinguer ?**

- A. Seulement la présence de texte.
- B. Seulement le code 200.
- C. Transport/délai, statut HTTP, format et contrat des données.

<details>
<summary>Afficher la réponse et l’explication</summary>

**Réponse C.** Transport/délai, statut HTTP, format et contrat des données.

Un HTTP réussi peut contenir un JSON invalide ou une réponse métier indisponible.

</details>

**Q10 — Dans la variante à plusieurs machines, Fabric collecte une seule des deux cibles demandées. Quelle conclusion
retenir ?**

- A. Le parc est en bon état.
- B. Conserver le succès et l’erreur, signaler la portée partielle, bloquer la diffusion complète.
- C. Supprimer la cible indisponible du résultat.

<details>
<summary>Afficher la réponse et l’explication</summary>

**Réponse B.** Conserver le succès et l’erreur, signaler la portée partielle, bloquer la diffusion complète.

L’erreur n’efface pas les observations disponibles ; un timeout ne démontre pas l’arrêt de la machine.

</details>

## Fin du jour 1 — 4 min

**Q11 — Quelle structure représente un couple fixe (hôte, port) ?**

- A. Un tuple.
- B. Un booléen.
- C. Une exception.

<details>
<summary>Afficher la réponse et l’explication</summary>

**Réponse A.** Un tuple.

Le tuple exprime ce regroupement fixe ; une liste sert aux suites modifiables.

</details>

**Q12 — Quel type permet de modifier directement un octet ?**

- A. str.
- B. bytearray.
- C. bytes.

<details>
<summary>Afficher la réponse et l’explication</summary>

**Réponse B.** bytearray.

bytes est immutable ; bytearray permet de remplacer une valeur entière de 0 à 255.

</details>

**Q13 — Quel bloc assure une action finale lorsqu’un try se termine avec ou sans exception ?**

- A. if.
- B. for.
- C. finally.

<details>
<summary>Afficher la réponse et l’explication</summary>

**Réponse C.** finally.

finally s’exécute à la sortie normale du try, y compris pendant la propagation d’une exception ; with est adapté à la
fermeture des fichiers.

</details>

**Q14 — Pourquoi csv.DictReader est-il préférable à split(";") pour un export CSV ?**

- A. Il prend en charge les champs cités et les séparateurs dans les valeurs.
- B. Il ignore toutes les lignes invalides.
- C. Il garantit que chaque IP est valide.

<details>
<summary>Afficher la réponse et l’explication</summary>

**Réponse A.** Il prend en charge les champs cités et les séparateurs dans les valeurs.

Le parseur traite la syntaxe CSV ; la validation des valeurs reste à écrire.

</details>

**Q15 — Pourquoi utiliser le garde `__name__ == "__main__"` ?**

- A. Pour installer Python.
- B. Pour lancer la démonstration directement sans la déclencher à l’import.
- C. Pour transformer chaque fonction en classe.

<details>
<summary>Afficher la réponse et l’explication</summary>

**Réponse B.** Pour lancer la démonstration directement sans la déclencher à l’import.

L’import rend les fonctions disponibles sans exécuter le scénario protégé.

</details>

## Fin du jour 2 — 4 min

**Q16 — Une IP produite par notre générateur est-elle libre sur le réseau ?**

- A. Oui, car elle appartient au sous-réseau.
- B. Oui, car elle est absente des réservations fournies.
- C. C’est une candidate ; aucune disponibilité réelle n’est démontrée.

<details>
<summary>Afficher la réponse et l’explication</summary>

**Réponse C.** C’est une candidate ; aucune disponibilité réelle n’est démontrée.

Il faut une procédure d’allocation et des vérifications adaptées au contexte réel.

</details>

**Q17 — Un timeout de commande signifie-t-il que le service est arrêté ?**

- A. Non, seulement que le résultat attendu n’a pas été obtenu dans le délai.
- B. Oui, toujours.
- C. Oui, si le code est écrit en Python.

<details>
<summary>Afficher la réponse et l’explication</summary>

**Réponse A.** Non, seulement que le résultat attendu n’a pas été obtenu dans le délai.

Conserver le délai et le contexte, puis effectuer les vérifications complémentaires.

</details>

**Q18 — Dans le format SSH du cours, l’IP après from identifie quoi ?**

- A. La cible.
- B. La source de la connexion.
- C. Le contrôleur Ansible.

<details>
<summary>Afficher la réponse et l’explication</summary>

**Réponse B.** La source de la connexion.

Le nom précédant sshd identifie la cible émettrice du log.

</details>

**Q19 — Un seuil de zéro refusé par argparse correspond à quel résultat ?**

- A. Une réussite avec zéro alerte.
- B. Un code SMTP.
- C. Une erreur d’usage, code de sortie 2.

<details>
<summary>Afficher la réponse et l’explication</summary>

**Réponse C.** Une erreur d’usage, code de sortie 2.

Le contrat demande un entier strictement positif ; l’échec doit être annoncé avant le traitement.

</details>

**Q20 — Comment conserver dans le rapport une IP de log absente de l’inventaire ?**

- A. Partir des événements et effectuer une jointure gauche, puis marquer les attributs inconnus.
- B. Utiliser obligatoirement une jointure interne.
- C. Remplacer l’IP par celle du poste local.

<details>
<summary>Afficher la réponse et l’explication</summary>

**Réponse A.** Partir des événements et effectuer une jointure gauche, puis marquer les attributs inconnus.

L’absence de correspondance reste une information ; vérifier aussi la cardinalité de la jointure.

</details>

## Fin du jour 3 — 4 min

**Q21 — Une erreur survient pendant l’insertion transactionnelle d’un rapport. Que doit-on faire ?**

- A. Annoncer une réussite partielle silencieuse.
- B. Annuler la transaction et signaler l’échec.
- C. Modifier le CSV pour supprimer la trace.

<details>
<summary>Afficher la réponse et l’explication</summary>

**Réponse B.** Annuler la transaction et signaler l’échec.

Le contrat vise un import atomique, sans base faussement complète.

</details>

**Q22 — Comment extraire l’état propre à chaque carte HTML avec Scrapy ?**

- A. Un seul sélecteur global recopié partout.
- B. Une requête SQL.
- C. Parcourir les cartes puis utiliser un sélecteur relatif à chacune.

<details>
<summary>Afficher la réponse et l’explication</summary>

**Réponse C.** Parcourir les cartes puis utiliser un sélecteur relatif à chacune.

Un sélecteur relatif évite de mélanger les données de plusieurs services.

</details>

**Q23 — Quelle preuve relie l’archive créée à la pièce reçue par le SMTP de capture ?**

- A. La comparaison des octets de la pièce avec le ZIP, puis de ses membres avec les sources.
- B. Le nom rapport.zip seulement.
- C. L’absence d’erreur dans l’éditeur.

<details>
<summary>Afficher la réponse et l’explication</summary>

**Réponse A.** La comparaison des octets de la pièce avec le ZIP, puis de ses membres avec les sources.

La soumission SMTP de test est prouvée ; une livraison externe et une lecture ne le sont pas.

</details>

**Q24 — Deux logs reçus contiennent le même événement. Peut-on éliminer automatiquement un doublon textuel ?**

- A. Oui, le texte suffit pour identifier un événement unique.
- B. Non ; conserver les sources et les lignes tant qu’une règle de déduplication n’est pas définie.
- C. Oui, si le seuil est 2.

<details>
<summary>Afficher la réponse et l’explication</summary>

**Réponse B.** Non ; conserver les sources et les lignes tant qu’une règle de déduplication n’est pas définie.

Des événements identiques peuvent provenir de deux cibles ; le manifeste conserve la provenance.

</details>

**Q25 — Quelle preuve attend-on après le deuxième passage du même playbook ?**

- A. Le mode check a créé le fichier.
- B. Un changement sur chaque cible.
- C. Aucun changement, aucune erreur et contenu/mode effectivement conformes.

<details>
<summary>Afficher la réponse et l’explication</summary>

**Réponse C.** Aucun changement, aucune erreur et contenu/mode effectivement conformes.

Idempotence observée sur ce scénario ; prévisualisation, application et relecture restent distinctes.

</details>
