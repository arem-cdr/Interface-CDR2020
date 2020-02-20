# :mag: Interface-CDR2020

Ce code servira à suivre en temps réel les variables internes du robot. Il tournera sur une raspberry pi connectée à une des cartes du robot. Chaque carte sera susceptible d'envoyer des données différentes, le code devra donc s'adapter à toutes les configurations possibles.


## :computer: Notes d'utilisation

- Le baudrate utilisé pour la communication est de **2 000 000**.

- Les unités utilisées sont les **ms** pour le temps, les **mm** pour les distances.

- Toutes les données envoyées devront être des **entiers**, à chaque fois suivis d'un **retour à la ligne**. Les valeurs **négatives** servent à indiquer quelles informations sont envoyées et marquent le début et la fin des communications. **Envoyer des valeurs négatives en dehors de ces cas d'utilisation causera une mauvaise lecture des données**.

- Afin de rendre le code capable de s'adapter à toutes les données entrantes (raspberry connectée à n'importe quelle carte ou bug de com), j'ai divisé les données entrantes sur la com en "séquences". Une séquence suivra toujours le schéma suivant :

| Code de la séquence < 0                                                     | Data ...               | -1                           |
| -------------------------                                                   | ----------             | ----                         |
| Marque le début d'une séquence et indique quelles données seront transmises | Contenu de la séquence | Marque la fin de la séquence |


Voici le tableau décrivant les différentes informations pouvant être transmises :

| Valeur | Catégorie   | Informations transmises                                                                  | Fin de séquence   |
| ------ | ----------  | -------------------------                                                                | ----------------- |
| -2     | Divers      | Reset                                                                                    | -1                |
| -3     | Divers      | Position du robot                                                                        | -1                |
| -4     | Divers      | Target du robot                                                                          | -1                |
| -5     | Divers      | Temps écoulé depuis boot                                                                 | -1                |
| -101   | Pathfinding | Obstacles perçus dans le pathfinding                                                     | -1                |
| -102   | Pathfinding | Arbre RRT généré                                                                         | -1                |
| -103   | Pathfinding | Nombre de noeuds dans RRT                                                                | -1                |
| -104   | Pathfinding | Chemin trouvé                                                                            | -1                |
| -201   | Asser       | {temps en ms, vitesses réelles roues droite et gauche, commandes roues droite et gauche} | -1                |

**Exemple** :
Le code suivant mettra à jour la target du robot à la position (1200, 450) :
```c++
Serial pc(USBTX, USBRX);

pc.baud(2000000);

pc.printf("%d\n", -4);
pc.printf("%d\n%d\n", 1200, 450);
pc.printf("%d\n", -1);
```


## :clipboard: ToDo

- [X] Créer une nouvelle classe AsserPlot permettant d'afficher un graphique qui aiderait à debug l'asser
- [X] Implémenter les séquences supportées par la classe AsserPlot
- [X] Créer un bouton Pause
- [ ] Créer une classe permettant d'afficher des info diverses modulable


## :memo: Fonctionnement du code

- Le rendu graphique est géré par l'extension pyqtGraph. Voir la [documentation de pyqtGraph](http://www.pyqtgraph.org/documentation/index.html) pour plus d'infos.

- Les classes sont organisées de la façon suivante :

| Nom de la classe | Fonction                                                                                                           |
| ---------------- | ----------                                                                                                         |
| App              | Gère la liaison série (framerate et lecture des données entrantes) et des variables globales à tous les graphiques |
| InterfaceDebug   | Gère la fenêtre de l'application, les différents graphiques ainsi que leur disposition dans l'espace               |
| MyPlot           | Classe commune à tous les graphiques initialisant des éléments de base                                             |
| PathfindingPlot  | Gère le graphique servant à débug le pathfinding, ainsi que toutes les variables qui lui sont associées            |
| AsserPlot        | Gère le graphique servant à débug l'asser, ainsi que toutes les variables qui lui sont associées                   |

- Les fonctions commençant par `processInputs_` permettent toutes de mettre à jour les données propres à chaque graphe en fonction des données entrant dans la liaison série.
