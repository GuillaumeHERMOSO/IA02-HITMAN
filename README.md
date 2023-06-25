# IA02-HITMAN

sujet : https://hackmd.io/@ia02/S1LNF3CMn

arbitre : https://gitlab.utc.fr/ia02/hitman 


# Projet IA02 - Hitman

...



## Prérequis

Avant d'exécuter le code, assurez-vous d'avoir les éléments suivants :

- *Le fichier hitman.py doit se trouver dans le dossier 'src/arbitre/'.*
- *L'executable gophersat doit se trouver dans le meme dossier que main.py*

- Python 3.x : le code est écrit en Python et nécessite une version 3.x du langage.

- Les modules suivants doivent être installés :
    - `os`
    - `pprint`
    - `random`
    - `time`
    - `itertools`
    - `typing`
    - `sys`
    - `copy`
    - `subprocess`


## Phase 1

### Strategie

- Appliquer une stratégie de début de partie.
- Tant que toutes les cases n'ont pas été explorées :

    - Trouver les cases inconnues les plus proches.
    - Prendre comme but la case inconnue la plus proche, accessible.
    - Appliquer l'algorithme A* pour trouver le chemin optimal vers la case permettant de voir la inconnue.
    - Transformer le chemin en une liste d'actions à exécuter.
    - Exécuter les actions, mettre à jour les connaissances et afficher si nécessaire.
    - Tourner le personnage dans la direction de la case inconnue.

### Heuristique 

On a eu besoin de plusieurs heuristiques pour résoudre le problème:
- distance de Manhattan, qui permet de trouver la case la plus proche de la case actuelle.
- la case ou on est est elle vu par un ennemi.

pas utilisé car pas assez performante:
- nbr de mur entre but et case actuelle
- distance euclidienne
- nombre de case inconnue proche
- nombre de case inconnue proche vu par un ennemi
- nombre de mur autour de la case inconnue
- nombre de case inconnue autour de la case inconnue
- nombre d'obstacle (garde ou mur) entre but et case actuelle





### Sat

Nous souhaitions utiliser le solveur SAT afin de déduire des informations, nous avons rencontrés plusieurs problèmes lors de son implémentation tel que : 
- La réecriture impossible d'un fichier SAT à partir de lui même (ce qui nous a contraint à devoir écrire un nouveau fichier de zéro à chaque fois et exploser le temps de calcul )
- Une gestion abérrante du nombre de clauses : Plus la map est grande, plus le nombre de clauses explose, ce qui nous a limité seulement à l'utilisation du solveur à la potentielle déduction des personnes (gardes et invités ) avec les clauses d'écoutes.
- Le plan était le suivant : 

    1) Trouver une/des variable(s) à déduire, les implémenter dans une liste
    2) Pour chaque élément de la liste, tester sa négation et voir si le solveur renvoie insatisfiable
    3) Si oui : inclure la nouvelle variable dans notre dico de connaissances et également dans nos clauses (en tant que clause unitaire)
    4) Si non : Ne rien déduire
- Pour la recherche des variables à déduire, nous nous étions limité aux variables dont la liste de clause possède pas déjà et qui ne sont pas déjà des clauses unitaires ( les variables qui sont présentes donc dans les clauses d'écoute), cela permettait de ne vouloir déduire que ce qui a déjà été évoqué.
- Le tableau de clause (ClauseBase donc liste de liste ) ne contenait que des clauses référents à des personnes soit vu par Hitman (unitaires) soit écoutés.
- La déduction a petit a petit commencé a devenir impossible du fait du nombre de clauses en fin d'exploration (~500 000), ce qui empêchait de continuer le parcours de la map (il fallait attendre plusieurs minutes par itération pour la map d'exemple qui est assez petite) .

C'est à causes de ces multiples problèmes que nous avons décidés de ne pas inclure la déduction par solveur SAT lors de la phase 1. 

#### modelisation:



## Phase 2

## Comment lancer le projet :

- Télécharger le dossier src et main.py
- Lancer le fichier main.py ( attendre quelques secondes, une carte devrait s'afficher )
- Pour la carte : "O" est Hitman et la flèche ("^",">","v","<") représente la direction dans laquelle il regarde actuellement, idem pour "G" : Garde et "C": Civil.
- X : Non découvert
- A : Arme (Corde de piano)
- S : Suit ( Le déguisement)
- "|" ou "-" : les murs de la carte 
