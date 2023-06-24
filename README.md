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

SAt utilise pour deduire des information ?

#### modelisation:



## Phase 2
