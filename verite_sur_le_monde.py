from pprint import pprint
from time import sleep
from typing import List, Tuple
import subprocess
from itertools import combinations

from contraintes import *
from affichage import *

Grid = List[List[int]]
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]
Model = List[Literal]


def recup_var_G(list_cases,dict_var_to_num):
    var = []
    for i in list_cases:
        #on recupere les variables du type 00_G mais pas 00_G_N
        if i[-1] == "G" :
            var.append(dict_var_to_num[i])

    return var
def gen_var_lettre(m,n,dict_var_to_num,lettre : str):
    var = []
    for i in range(m):
        for j in range(n):
            var.append(dict_var_to_num[f"{i}{j}_{lettre}"])
    return var

def gen_var_par_case(m,n,list_cases,dict_var_to_num, sauf :list[str] =["P","G","I"]):
    # {"00": ["00_V","00_M","00_C",...,"00_G_O"]
    #  "01": ["01_V",...,"01_G_O"]
    #  ...}
    dico_var_par_case = {}
    for i in range(m):
        for j in range(n):
            dico_var_par_case[f"{i}{j}"] = []
    
    for k in list_cases:
        if k[-1] not in sauf:
            dico_var_par_case[k[:2]].append(dict_var_to_num[k])
    return dico_var_par_case 

#00_P<-> 00_Gou 00_i  : (-00_P ou 00_G ou 00_I ) et (-00_G ou 00_P) et (-00_I  ou 00_P)
def gen_clause_P_equi_G_ou_I(m,n,dict_var_to_num):
    r: ClauseBase = []
    #on genere les variables
    var_P = gen_var_lettre(m,n,dict_var_to_num,"P")
    var_G = gen_var_lettre(m,n,dict_var_to_num,"G")
    var_I = gen_var_lettre(m,n,dict_var_to_num,"I")
    for i in range(len(var_P)):
        r.append([-var_P[i],var_G[i],var_I[i]])
        r.append([-var_G[i],var_P[i]])
        r.append([-var_I[i],var_P[i]])
    return r

def gen_clause_lettre_equi_lettre_orientation(m,n,dict_var_to_num,lettre : str):
    r: ClauseBase = []
    #on genere les variables
    var_l = gen_var_lettre(m,n,dict_var_to_num,f"{lettre}")
    var_l_N = gen_var_lettre(m,n,dict_var_to_num,f"{lettre}_N")
    var_l_S = gen_var_lettre(m,n,dict_var_to_num,f"{lettre}_S")
    var_l_E = gen_var_lettre(m,n,dict_var_to_num,f"{lettre}_E")
    var_l_O = gen_var_lettre(m,n,dict_var_to_num,f"{lettre}_O")
    for i in range(len(var_l)):
        r.append([-var_l[i],var_l_N[i],var_l_S[i],var_l_E[i],var_l_O[i]])
        r.append([-var_l_N[i],var_l[i]])
        r.append([-var_l_S[i],var_l[i]])
        r.append([-var_l_E[i],var_l[i]])
        r.append([-var_l_O[i],var_l[i]])
    return r



#Écrire une fonction clauses_to_dimacs(clauses: ClauseBase, nb_vars: int) -> str qui,
#étant donné une base de clauses et le nombre de variables à considérer, renvoie une
#chaîne de caractères codant la base de clauses au format Dimacs.
#>>> clauses_to_dimacs([[-1, -2], [1, 2], [1, 3], [2, 4], [-3, 4], [-4, 5]], 5)
#'p cnf 5 6\n-1 -2 0\n1 2 0\n1 3 0\n2 4 0\n-3 4 0\n-4 5 0\n'

def clauses_to_dimacs(clauses: ClauseBase, nb_vars: int) -> str:
    r = f"p cnf {nb_vars} {len(clauses)}\n"
    for clause in clauses:
        for literal in clause:
            r += f"{literal} "
        r += "0\n"
    return r




def main():
    list_var = creer_list_var(5,8)
    dico_var_to_num = creer_dictionnaire_cases_par_list(list_var)

    #on recupere les variables
    var_Guarde =  gen_var_lettre(5,8,dico_var_to_num,"G")
    var_Target =  gen_var_lettre(5,8,dico_var_to_num,"T")
    var_Invite =  gen_var_lettre(5,8,dico_var_to_num,"I")
    var_Corde  =  gen_var_lettre(5,8,dico_var_to_num,"C")
    dico_par_case = gen_var_par_case(5,8,list_var,dico_var_to_num)


    #on genere les clauses
    V_sur_le_monde : ClauseBase = []
    V_sur_le_monde += exactly_k(2,var_Guarde)
    V_sur_le_monde += exactly_k(3,var_Invite)
    V_sur_le_monde += exactly_k(1,var_Target)
    V_sur_le_monde += exactly_k(1,var_Corde)
    for i in dico_par_case:
        V_sur_le_monde += exactly_k(1,dico_par_case[i])

    V_sur_le_monde += gen_clause_P_equi_G_ou_I(5,8,dico_var_to_num)
    V_sur_le_monde += gen_clause_lettre_equi_lettre_orientation(5,8,dico_var_to_num,"G")
    V_sur_le_monde += gen_clause_lettre_equi_lettre_orientation(5,8,dico_var_to_num,"I")

    print(len(list_var))
    print(len(V_sur_le_monde))

    dimac = clauses_to_dimacs(V_sur_le_monde,len(list_var))
    #print(dimac)
    write_dimacs_file(dimac, "./test.cnf")
    res = exec_gophersat( "test.cnf")
    
    print(res)
    model_to_grid(res[1],5,8,list_var)

    pass


if __name__ == "__main__":
    main()