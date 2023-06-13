from pprint import pprint
from time import sleep
from typing import List, Tuple
import subprocess
from itertools import combinations

from src.arbitre.hitman import *
from src.contraintes import *
from src.arbitre.hitman import *
from src.sat import *

import Class_HitmanKnowledge

Grid = List[List[int]]
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = set[Clause]
Model = List[Literal]

def ecouter(seta : set, dico : HitmanReferee.start_phase1(),dict_var_to_num) : # ecouter avec l'arbitre

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
        return add_list_to_set(seta,at_least_k(5,r)) # Si on entend au moins 5 personnes

    return add_list_to_set(seta,exactly_k(k,r))  # Si on entend moins de 5 personnes

def add_voir(seta : set,dict_var_to_num, dico : Class_HitmanKnowledge.HitmanKnowledge) : # Voir pour le sat
    variables = []
    for pos,valeur in dico.affichage_vison() :
        x,y = pos
        variables.append(dict_var_to_num[f"{x}{y}_P"])  # Transformation en valeurs utilisable dans SAT
    return add_list_to_set(seta,variables)

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

def ajout_vision_garde (dico,pos,garde,dico_connaissance,matrice_vision) : # on incremente les case vu dans la matrice
    n = dico["n"]
    m = dico["m"]
    offset_x, offset_y = orientation_garde(garde)
    x, y = pos
    vision = []
    for _ in range(0, 2):
        pos = x + offset_x, y + offset_y
        x, y = pos
        if x >= n or y >= m or x < 0 or y < 0:
            break
        vision.append(pos)
        if dico_connaissance[pos] != HC.EMPTY and matrice_vision[x][y] == 0: # Si dans notre matrice de connaissance
                                                # on sait ce qu'il y a a la 2e case du champ de vision du garde
            break
    for x,y in vision :
        matrice_vision[x][y] += 1
    return matrice_vision

def maj_dico_connaissance(dico_connaissance,dico) : # Voir pour notre dico
    for pos, valeur in  dico["vision"]:
        dico_connaissance[pos] = valeur
    return dico_connaissance

def maj_fichier_sat_vision(dico) :
    # mise a jour du fichier sat en appelant voir
    pass
def avancer(dico,dico_connaissance,matrice_vision) :
    x,y = dico["position"]
    n = dico["n"]
    m = dico["m"]
    pos = x,y
    compteur = []
    if dico["orientation"] == HC.N:
        orientation = 0, 1
    elif dico["orientation"] == HC.E:
        orientation = 1, 0
    elif dico["orientation"] == HC.S:
        orientation = 0, -1
    elif dico["orientation"] == HC.W:
        orientation = -1, 0

    if x<n and dico_connaissance[(x + 1, y)] == "Vide" : # Si le nord est inconnu
        if orientation == (1, 0):  # Si à l'est
            dico = HitmanReferee.turn_clockwise()
            dico_connaissance = maj_dico_connaissance(dico_connaissance,dico)
            maj_fichier_sat_vision(dico)
        else:  # Si Ouest ou Sud(opposé de nord )
            dico = HitmanReferee.turn_anti_clockwise()
            dico_connaissance = maj_dico_connaissance(dico_connaissance,dico)
            maj_fichier_sat_vision(dico)

    if x>0 and dico_connaissance[(x - 1, y)] == "Vide": # Si le sud est inconnu
        if orientation == (-1, 0):  # Si à l'ouest
            dico = HitmanReferee.turn_clockwise()
            dico_connaissance = maj_dico_connaissance(dico_connaissance,dico)
            maj_fichier_sat_vision(dico)
        else:  # Si Est ou nord(opposé de sud )
            dico = HitmanReferee.turn_anti_clockwise()
            dico_connaissance = maj_dico_connaissance(dico_connaissance,dico)
            maj_fichier_sat_vision(dico)


    if y<m and dico_connaissance[(x, y+1)] == "Vide": # Si l'est est inconnu
        if orientation == (0, 1):  # Si au Nord
            dico = HitmanReferee.turn_clockwise()
            dico_connaissance = maj_dico_connaissance(dico_connaissance,dico)
            maj_fichier_sat_vision(dico)

        else:  # Si Sud ou Ouest(opposé de l'est )
            dico = HitmanReferee.turn_anti_clockwise()
            dico_connaissance = maj_dico_connaissance(dico_connaissance,dico)
            maj_fichier_sat_vision(dico)


    if y>0 and dico_connaissance[(x, y - 1)] == "Vide": # Si l'ouest est inconnu
        if orientation == (0, -1):  # Si au Sud
            dico = HitmanReferee.turn_clockwise()
            dico_connaissance = maj_dico_connaissance(dico_connaissance,dico)
            maj_fichier_sat_vision(dico)

        else:  # Si Nord ou Est (opposé de l'ouest )
            dico = HitmanReferee.turn_anti_clockwise()
            dico_connaissance = maj_dico_connaissance(dico_connaissance,dico)
            maj_fichier_sat_vision(dico)

    # Normalement d'ici on a toutes les données des 4 orientations

    if orientation == (0,1) and x<n and matrice_vision[x+1][y] == 0 and dico_connaissance[(x+1,y)] not in [HC.WALL,HC.GUARD_W,HC.GUARD_N,HC.GUARD_E,HC.GUARD_S] :
        return HitmanReferee.move()
    if orientation == (0,-1) and x>0 and matrice_vision[x-1][y] == 0 and dico_connaissance[(x-1,y)] not in [HC.WALL,HC.GUARD_W,HC.GUARD_N,HC.GUARD_E,HC.GUARD_S] :
        return HitmanReferee.move()
    if orientation == (1,0) and y<m and matrice_vision[x][y+1] == 0 and dico_connaissance[(x,y+1)] not in [HC.WALL,HC.GUARD_W,HC.GUARD_N,HC.GUARD_E,HC.GUARD_S] :
        return HitmanReferee.move()
    if orientation == (-1,0) and y>0 and matrice_vision[x][y-1] == 0 and dico_connaissance[(x,y-1)] not in [HC.WALL,HC.GUARD_W,HC.GUARD_N,HC.GUARD_E,HC.GUARD_S] :
        return HitmanReferee.move()

    return dico
