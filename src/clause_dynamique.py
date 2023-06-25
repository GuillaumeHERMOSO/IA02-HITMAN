from pprint import pprint
from time import sleep
from typing import List, Tuple
import subprocess
from itertools import combinations

from src.arbitre.hitman import *
from src.contraintes import *
from src.arbitre.hitman import *
from src.sat import *

from src.Class_HitmanKnowledge import *

Grid = List[List[int]]
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]
Model = List[Literal]

def ecouter(hr : HitmanReferee,dict_var_to_num) : # ecouter avec l'arbitre
    """ Fonction qui permet de créer les clauses pour la contrainte ecouter """
    # On récupère les valeurs du dico de l'arbitre :
    dico = hr.start_phase1()
    k = dico["hear"]
    n = dico["n"]
    m = dico["m"]
    i,j = dico["position"]
    r = []
    variables = []
    
    for a in range(i-2,i+3):
        for b in range(j-2,j+3):
            if a in range(n) and b in range(m) and (a,b) != (i,j):
                variables.append(f"{a}{b}_P")
    
    for elt in variables :
        r.append(dict_var_to_num[elt]) # Transformation en valeurs utilisable dans SAT
    if k >= 5:
        return at_least_k(5,r) # Si on entend au moins 5 personnes
    return exactly_k(k,r)  # Si on entend moins de 5 personnes


def orientation_garde(garde):
    if garde == HC.GUARD_N:
        offset = 0, 1
    elif garde == HC.GUARD_E:
        offset = 1, 0
    elif garde == HC.GUARD_S:
        offset = 0, -1
    elif garde == HC.GUARD_W:
        offset = -1, 0

    return offset

