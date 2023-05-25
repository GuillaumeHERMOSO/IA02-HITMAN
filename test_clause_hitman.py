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


# ["00_V","00_M","00_C",...,"00_G_O","01_V",...,"58_G_O"]
def creer_list_var(m,n):
    list_cases = []
    for i in range(0,m):
        for j in range(0,n):
            for reste in ["V","M","C","D","T","I","I_N","I_S","I_E","I_O","G","G_N","G_S","G_E","G_O","P"]:
                list_cases.append("%d%d_%s"%(i,j,reste))
    return list_cases


def creer_dictionnaire_cases_par_list(list_variable):
    # Création du dictionnaire une variable = un chiffre:
    compteur = 1
    dict_cases = {}
    for i in list_variable:
        dict_cases[i] = compteur
        compteur += 1
    return dict_cases

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
