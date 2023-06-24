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

    # On récupère les valeurs du dico de l'arbitre :
    dico = hr.start_phase1()
    k = dico["hear"]
    n = dico["n"]
    m = dico["m"]
    i,j = dico["position"]
    r = []
    min_i = max_i = min_j = max_j = 0 # initialisation des bornes i et j
    variables = []
    if (i == 0 or i == 1): # si i est dans la borne inf ou a 1 de distance de celle ci
        min_i,max_i = ( 0 , i + 2 )
    elif (i == n or i == n - 1 ) :
        min_i,max_i = ( i - 2 , n )
    else :              # sinon : cas general
        min_i, max_i = (i - 2, i + 2 )

    if (j == 0 or j == 1):  # si j est dans la borne inf ou a 1 de distance de celle ci
        min_j, max_j = (0, j + 2)
    elif (j == m or j == m - 1) :
        min_j, max_j = (j - 2, m)
    else:                   # sinon : cas general
        min_j, max_j = (j - 2, j + 2)

    for a in range(min_i,max_i):
        for b in range(min_j, max_j):
            variables.append(f"{a}{b}_P")       # on génère nos variables

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


def maj_fichier_sat_vision(dico) :
    # mise a jour du fichier sat en appelant voir
    pass
