from pprint import pprint
from time import sleep
from typing import List, Tuple
import subprocess
from itertools import combinations
Grid = List[List[int]]
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]
Model = List[Literal]

#map m*n de taille


#vide 					V
#mur 					M
#corde de piano 		C
#costume deguisement 	D
#cible 					T
#invité (N/S/E/O)		I
#garde (N/S/E/O)		G

#variable du type
#position__type_orientation
#00_V
#00_I_N

#{"00" = ["00_V","00_M","00_C","00_D","00_T","00_I_N","00_I_S","00_I_E","00_I_O","00_G_N","00_G_S","00_G_E","00_G_O""]}
def creer_dico_var(m,n):
    dict_cases = {}
    for i in range(1,m+1):
        for j in range(1,n+1):
            dict_cases["%d%d"%(i,j)] = ["%d%d_V"%(i,j),"%d%d_M"%(i,j),"%d%d_C"%(i,j),"%d%d_D"%(i,j),"%d%d_T"%(i,j),"%d%d_I_N"%(i,j),"%d%d_I_S"%(i,j),"%d%d_I_E"%(i,j),"%d%d_I_O"%(i,j),"%d%d_G_N"%(i,j),"%d%d_G_S"%(i,j),"%d%d_G_E"%(i,j),"%d%d_G_O"%(i,j)]
    return dict_cases
#print(creer_dico_var(m=2,n=2))

# ["00_V","00_M","00_C",...,"00_G_O","01_V",...,"58_G_O"]
def creer_list_var(m,n):
    list_cases = []
    for i in range(0,m):
        for j in range(0,n):
            for reste in ["V","M","C","D","T","I","I_N","I_S","I_E","I_O","G","G_N","G_S","G_E","G_O"]:
                list_cases.append("%d%d_%s"%(i,j,reste))
    return list_cases
#print(creer_list_var(m=2,n=2))


def creer_dictionnaire_cases_par_dico(dict_variable):
    # Création du dictionnaire une variable = un chiffre:
    compteur = 1
    dict_cases = {}
    for position in dict_variable.keys():
        for i in dict_variable[position]:
            dict_cases[i] = compteur
            compteur += 1
    return dict_cases

def creer_dictionnaire_cases_par_list(list_variable):
    # Création du dictionnaire une variable = un chiffre:
    compteur = 1
    dict_cases = {}
    for i in list_variable:
        dict_cases[i] = compteur
        compteur += 1
    return dict_cases
#print(creer_dictionnaire_cases_par_dico(creer_dico_var(m=2,n=2)))
#print(creer_dictionnaire_cases_par_list(creer_list_var(m=2,n=2)))

def at_least_one(v: List[PropositionnalVariable]) -> Clause:
    return v

def unique(variables: List[PropositionnalVariable]) -> ClauseBase:
    r: ClauseBase = [at_least_one(variables)]
    for a, b in combinations(variables, 2):
        r.append([-a, -b])
    print(r)
    return r

#### fonctions fournies

def write_dimacs_file(dimacs: str, filename: str):
    with open(filename, "w", newline="") as cnf:
        cnf.write(dimacs)

def exec_gophersat(
    filename: str, cmd: str = "gophersat", encoding: str = "utf8"
) -> Tuple[bool, List[int]]:
    result = subprocess.run(
        [cmd, filename], capture_output=True, check=True, encoding=encoding
    )
    string = str(result.stdout)
    lines = string.splitlines()


    if lines[1] != "s SATISFIABLE":
        return False, []


    model = lines[2][2:-2].split(" ")


    return True, [int(x) for x in model]


#clause verité sur le monde
def clause_il_y_a_K_garde(m,n,k):
    #variables = ["00","01", .."08","10","11",..."18",..."57","58"]
    variables = []
    r: ClauseBase = []
    for i in range(0,m):
        for j in range(0,n):
            variables.append("%d%d_G"%(i,j))
    #creation d'un tableau de taille k pour recuperer les variable des combinaisons

    for tab in combinations(variables, k+1):
        r.append(["-"+ x for x in tab])
    for tab in combinations(variables, len(variables)+1-k):
        r.append([x for x in tab])
    return r

def clause_il_y_a_K_invite(m,n,k):
        #variables = ["00","01", .."08","10","11",..."18",..."57","58"]
    variables = []
    r: ClauseBase = []
    for i in range(0,m):
        for j in range(0,n):
            variables.append("%d%d_I"%(i,j))
    #creation d'un tableau de taille k pour recuperer les variable des combinaisons

    for tab in combinations(variables, k+1):
        r.append(["-"+ x for x in tab])
    for tab in combinations(variables, len(variables)+1-k):
        r.append([x for x in tab])
    return r

def clause_une_cible(m,n):
    variables = []
    r: ClauseBase = []
    for i in range(0,m):
        for j in range(0,n):
            variables.append("%d%d_T"%(i,j))
    #creation d'un tableau de taille k pour recuperer les variable des combinaisons
    for tab in combinations(variables, 2):
        r.append(["-"+ x for x in tab])
    for tab in combinations(variables, len(variables)+1-2):
        r.append([x for x in tab])
    return r

def clause_une_corde(m,n):
    variables = []
    r: ClauseBase = []
    for i in range(0,m):
        for j in range(0,n):
            variables.append("%d%d_C"%(i,j))
    #creation d'un tableau de taille k pour recuperer les variable des combinaisons
    for tab in combinations(variables, 2):
        r.append(["-"+ x for x in tab])
    for tab in combinations(variables, len(variables)+1-2):
        r.append([x for x in tab])
    return r

def clause_un_deguisement(m,n):
    variables = []
    r: ClauseBase = []
    for i in range(0,m):
        for j in range(0,n):
            variables.append("%d%d_D"%(i,j))
    #creation d'un tableau de taille k pour recuperer les variable des combinaisons
    for tab in combinations(variables, 2):
        r.append(["-"+ x for x in tab])
    for tab in combinations(variables, len(variables)+1-2):
        r.append([x for x in tab])
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
    m=5
    n=8
    l_var = creer_list_var(m,n)
    dict_var_to_num = creer_dictionnaire_cases_par_list(l_var)

    print(recup_var_G(l_var,dict_var_to_num))
    for i in recup_var_G(l_var,dict_var_to_num):
        key = [k  for (k, val) in dict_var_to_num.items() if val == i]
        print(key)

    clause_2_garde = exactly_k(2,recup_var_G(l_var,dict_var_to_num))
    clause_2_garde_v1 = clause_il_y_a_K_garde(m,n,2)
    print(len(clause_2_garde))
    print(len(clause_2_garde_v1))
    
    pass


if __name__ == "__main__":
    main()
