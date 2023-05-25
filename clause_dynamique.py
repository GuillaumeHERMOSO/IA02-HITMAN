from pprint import pprint
from time import sleep
from typing import List, Tuple
import subprocess
from itertools import combinations

from contraintes import *

from hitman import HC, HitmanReferee

Grid = List[List[int]]
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]
Model = List[Literal]

def ecouter(dico,dict_var_to_num) : # ecouter avec l'arbitre

    # On récupère les valeurs du dico de l'arbitre :
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

def voir(dico,dict_var_to_num) : # Voir comme on le pense maintenant ( avec l'arbitre )
    liste = dico["vision"]
    variables = []
    for pos,valeur in liste :
        x,y = pos
        variables.append(dict_var_to_num[f"{x}{y}_{valeur}"])  # Transformation en valeurs utilisable dans SAT
    return variables




def recup_var_G(list_cases,dict_var_to_num):
    var = []
    for i in list_cases:
        #on recupere les variables du type 00_G mais pas 00_G_N
        if i[-1] == "G" :
            var.append(dict_var_to_num[i])

    return var


def main():

    pass


if __name__ == "__main__":
    main()