# Dépannage

[Retour à l’accueil](../README.md)

| Message ou symptôme | Action |
| --- | --- |
| uv introuvable | Rouvrez le terminal Linux après installation ; revenez au [guide](installation.md) |
| pyproject.toml introuvable | Vérifiez pwd puis ouvrez le terminal à la racine du projet complet |
| ModuleNotFoundError | Lancez uv sync --locked, puis utilisez uv run plutôt que le Python global |
| Ansible introuvable | Lancez uv sync --locked dans Linux ; le groupe distant est inclus par défaut |
| Votre modification ne change rien | Enregistrez le fichier ; vérifiez le poste, l’interpréteur et le nom du script exécuté |
| À compléter ou À revoir | Consultez l’étape et les différences attendues/obtenues ; le départ est volontairement incomplet |
| Le contrôle principal passe, --complet échoue | Complétez les étapes intermédiaires indiquées |
| Téléchargement impossible | Vérifiez Internet et le proxy ; conservez uv.lock |
| Refus d’écriture | Travaillez dans votre dossier utilisateur et contrôlez le diagnostic du projet |
| Inventaire absent | Suivez le [guide SSH](../laboratoire/README.md) ; vérifiez le chemin PYX_INVENTAIRE si utilisé |
| Clé d’hôte refusée | Comparez l’identité de la cible avec les informations d’accès vérifiées ; ne désactivez pas le contrôle |
| Connexion SSH impossible | Vérifiez adresse, port, utilisateur, clé et disponibilité du service ; bureau distant et SSH sont des accès distincts |
| Collecte partielle | Lire collecte.csv ; conserver les succès et examiner la cible en erreur avant de diffuser |
| Premier passage Ansible sans changement | L’état était peut-être déjà conforme ; le second doit aussi conserver cet état |
| 127.0.0.1 ne répond pas dans le navigateur personnel | Le service local tourne dans le poste Linux ; utilisez le client fourni dans ce poste |
| Port des cibles Docker déjà utilisé | Les ports 22231/22232 concernent seulement le secours ; identifier le programme avant de l’arrêter |

Pour demander de l’aide, copiez la commande, le message complet et le nom du TP. Indiquez le dossier courant et ce que
vous attendiez. Gardez les clés privées et les mots de passe hors des messages.

## Lire une erreur Python

Lire la dernière ligne du traceback pour le type et le message, puis la dernière ligne de votre propre code pour
localiser l’opération. Examiner la valeur et son type ; pour un fichier, vérifier le dossier courant et le chemin
résolu. Corriger une cause puis refaire le même essai. Les
[cas de débogage et le mémo](memo-python-uv.md#erreurs-et-débogage) donnent deux exemples manipulables.
