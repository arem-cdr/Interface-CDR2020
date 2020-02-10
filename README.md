# :mag: Interface-CDR2020

------------------------------------------------------------------------

Ce code servira à suivre en temps réel les variables internes du robot. Il tournera sur une raspberry pi connectée à une des carte du robot. Chaque carte sera susceptible d'envoyer des données différentes, le code devra donc s'adapter à toutes les configurations possibles.

-----
**:computer: Notes d'utilisation**
-

- Veiller à modifier 'com8' par le port auquel la carte est branchée dans le main à la ligne `ser = serial.Serial('com8', 2000000)`. Pour connaitre les ports probables, utiliser la commande `python -m serial.tools.list_ports -v` dans un terminal.
- Toutes les données envoyées sur la com doivent être positives car j'utilise des valeurs négatives pour connaitre quel donnée va être envoyées à la prochaine com.

-----

**:clipboard: ToDo:**
-
- [X] Créer une nouvelle classe AsserPlot permettant d'afficher un graphique qui aiderait à debug l'asser
- [ ] Implémenter les séquences supportées par la classe AsserPlot
- [ ] Créer une classe permettant d'afficher des info diverses modulable 


---
**:memo: Fonctionnement du code :**
-

- Le rendu graphique est gérée par l'extension pyqtGraph. Cf http://www.pyqtgraph.org/documentation/index.html de pyqtGraph pour plus d'infos.
- Afin de rendre le code capable de s'adapter à toutes les données entrantes (raspi connectée à n'importe quelle carte ou bug de com), j'ai divisé les données entrantes sur la com en "séquences". Une séquence suivra toujours ce shéma : 

| Code de la séquence < 0 | Data ... | -1 |
|-------------------------|----------|----|
| Marque le début d'une séquence et indique quelles données seront transmises | Contenu de la séquence | Marque la fin de la séquence |

- Le code de séquence utilisé est le suivant :

| Catégorie| Valeur | Informations transmises |
|----------|--------|-------------------------|
| Divers | -1 | Fin de com |
| Divers | -2 | Position du robot |
| Divers | -3 | Target du robot |
| Divers | -4 | Temps écoulé depuis boot |
| Pathfinding | -101 | Obstacles perçus dans le pathfinding |
| Pathfinding | -102 | Arbre RRT généré |
| Pathfinding | -103 | Nombre de noeuds dans RRT |
| Pathfinding | -104 | Chemin trouvé |

