from pprint import pprint
from time import sleep
from typing import List, Tuple
import subprocess
from itertools import combinations

from test_clause_hitman import *
Grid = List[List[int]]
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]
Model = List[Literal]


def ecouter(i,j,m,n, matrice,dict_var_to_num) : # ici (0,0) = coin inferieur gauche
    r = []
    variables = []
    k = 0
    if i == 0 :
        if j == 0 : # coin inférieur gauche
            for a, b in combinations([1,0],2) :
                if (matrice[a][b] == "G" or matrice[a][b] == "I") :
                    k+= 1
                variables.append(f"{a}{b}_P")
        elif j == m : # coin inférieur droit
            for a in range(0,1) :
                for b in range(m-1,m) :
                    if (matrice[a][b] == "G" or matrice[a][b] == "I"):
                        k += 1
                    variables.append(f"{a}{b}_P")
        else :
            for a in range(0,1) :
                for b in range(j-1,j+1) :
                    if (matrice[a][b] == "G" or matrice[a][b] == "I"):
                        k += 1
                    variables.append(f"{a}{b}_P")
    elif i == n :
        if j == 0 :  # coin supérieur gauche
            for a in range(n-1,n) :
                for b in range(0,1) :
                    if (matrice[a][b] == "G" or matrice[a][b] == "I"):
                        k += 1
                    variables.append(f"{a}{b}_P")
        elif j == m : # coin supérieur droit
            for a in range(n-1,n) :
                for b in range(m-1,m) :
                    if (matrice[a][b] == "G" or matrice[a][b] == "I"):
                        k += 1
                    variables.append(f"{a}{b}_P")
        else :
            for a in range(n-1,n) :
                for b in range(j-1,j+1) :
                    if (matrice[a][b] == "G" or matrice[a][b] == "I"):
                        k += 1
                    variables.append(f"{a}{b}_P")
    else :
        for a in range(i-1, i+1):
            for b in range(j - 1, j + 1):
                if (matrice[a][b] == "G" or matrice[a][b] == "I"):
                    k += 1
                variables.append(f"{a}{b}_P")
    for elt in variables :
        r.append(dict_var_to_num[elt])
    return exactly_k(k,r)

def voir(i,j,m,n,orientation,matrice,dict_var_to_num) :
    r = []
    variables = []
    if orientation == "E"  :
        if j == m : # Si face a la bordure de droite on ne fait rien
            return
        if matrice(i,j+1) != "V" and j+1<=m : # Si la case d'après est non vide
            variables.append(matrice(i,j+1)) # ou modifier la matrice dynamique ( pas "matrice", la deuxieme vide qui se remplit au fur et a mesure )
        elif matrice(i,j+2) != "V" and j+2<=m:
            variables.append(matrice(i, j + 1))
            variables.append(matrice(i, j + 2))
        elif matrice(i,j+3) != "V" and j+3<=m:
            variables.append(matrice(i, j + 1))
            variables.append(matrice(i, j + 2))
            variables.append(matrice(i, j + 3))
        else :        # Si toute les cases ( 3 ) sont vides
            variables.append(matrice(i, j + 1))
            variables.append(matrice(i, j + 2))
            variables.append(matrice(i, j + 3))
    elif orientation == "O"  :
        if j == 0 :
            return
        if matrice(i,j-1) != "V" and j-1>=0 :
            variables.append(matrice(i,j-1))
        elif matrice(i,j-2) != "V" and j-2>=0:
            variables.append(matrice(i, j - 1))
            variables.append(matrice(i, j - 2))
        elif matrice(i,j-3) != "V" and j-3>=0:
            variables.append(matrice(i, j - 1))
            variables.append(matrice(i, j - 2))
            variables.append(matrice(i, j - 3))
        else :
            variables.append(matrice(i, j - 1))
            variables.append(matrice(i, j - 2))
            variables.append(matrice(i, j - 3))
    elif orientation == "S":
        if i == 0 :
            return
        elif matrice(i-1,j) != "V" and i-1>=0 :
            variables.append(matrice(i-1,j))
        elif matrice(i-2,j) != "V" and i-2>=0:
            variables.append(matrice(i-1, j ))
            variables.append(matrice(i-2, j ))
        elif matrice(i-3,j) != "V" and i-3>=0:
            variables.append(matrice(i-1, j ))
            variables.append(matrice(i-2, j ))
            variables.append(matrice(i-3, j ))
        else :
            variables.append(matrice(i-1, j ))
            variables.append(matrice(i-2, j ))
            variables.append(matrice(i-3, j ))
    else : # orientation == "N":
        if i == n :
            return
        elif matrice(i+1,j) != "V" and i+1<=n :
            variables.append(matrice(i+1,j))
        elif matrice(i+2,j) != "V" and i+2<=n:
            variables.append(matrice(i+1, j ))
            variables.append(matrice(i+2, j ))
        elif matrice(i+3,j) != "V" and i+3<=n:
            variables.append(matrice(i+1, j ))
            variables.append(matrice(i+2, j ))
            variables.append(matrice(i+3, j ))
        else :
            variables.append(matrice(i+1, j ))
            variables.append(matrice(i+2, j ))
            variables.append(matrice(i+3, j ))
    for elt in variables :
        r.append(dict_var_to_num[elt])
    return r


def recup_var_G(list_cases,dict_var_to_num):
    var = []
    for i in list_cases:
        #on recupere les variables du type 00_G mais pas 00_G_N
        if i[-1] == "G" :
            var.append(dict_var_to_num[i])

    return var

def exactly_k(k: int, variables: List[PropositionnalVariable]) -> ClauseBase:
    r: ClauseBase = []
    for tab in combinations(variables, k+1):
        r.append([-x for x in tab])
    for tab in combinations(variables, len(variables)+1-k):
        r.append([x for x in tab])
    return r

def main():

    pass


if __name__ == "__main__":
    main()