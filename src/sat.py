from typing import List, Dict, Tuple
import subprocess
Grid = List[List[int]]
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]
Model = List[Literal]
from src.Class_HitmanKnowledge import *


def creer_list_var(m: int, n: int) -> list:
    """ Fonction qui permet de créer la liste des variables """
    list_cases = []
    for j in range(0,m):
        for i in range(0,n):
                list_cases.append("%d%d_%s"%(i,j,"P"))
    return list_cases

def creer_dictionnaire_cases_par_list(list_variable : list) -> Tuple[dict,int]:
    """ Fonction qui permet de créer un dictionnaire qui associe une variable à un chiffre"""
    # Création du dictionnaire une variable = un chiffre:
    compteur = 0
    dict_cases = {}
    for var in list_variable:  # var = "ij_P"
        compteur += 1
        dict_cases[var] = compteur

    return dict_cases, compteur

def write_dimacs_file2(clauses: ClauseBase, nb_vars: int, filename: str):
    r = ["p cnf", str(nb_vars), str(len(clauses))]
    i = 0

    with open(filename, "w", newline="") as cnf:
        cnf.write(" ".join(r) + "\n")
        
        for clause in clauses:
            clause_str = " ".join(map(str, clause)) + " 0\n"
            cnf.write(clause_str)
            
            # Affichage du compteur de progression
            print(i, end="\r")
            i += 1

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



def deduction(dict_var_to_num : dict,hc : HitmanKnowledge,Clauses : ClauseBase, nb_vars: int, var_tester: int):
    """ Fonction qui permet de déduire des informations"""
    
    # on creer un fichier de clauses
    temp = Clauses +[[-var_tester]]
    write_dimacs_file2(temp, nb_vars, "sat.cnf")
    #on test la deduction
    res = exec_gophersat("sat.cnf")

    if res[0] == False:
        print(f"on deduit  : {trouver_cle(dict_var_to_num,var_tester)}")
        pos = trouver_cle(dict_var_to_num,var_tester) # On récupère les coordonnées de l'individu déduit
        pos = (int(pos[0]),int(pos[1]))
        hc.add_knowledge(pos,HC.N)   # Ajout d'un individu déduit

        return  Clauses +[[var_tester]]
    elif res[0] == True:
        #print(f"on n'a pas pu déduire :  {trouver_cle(dict_var_to_num,var_tester)}")
        pass

    return Clauses


def boucle_deduction2(dict_var_to_num : dict,hc : HitmanKnowledge,clauses : ClauseBase, nb_vars : int) -> ClauseBase:
    temp = clauses
    # on prend les x qui sont pas dans les connaissance entre (0,0) et (m,n)
    list_var = hc.get_no_knowledge_clause(dict_var_to_num)
    #print(f"on doit tester : {list_var}")
    for var in list_var:
        temp = deduction(dict_var_to_num,hc,temp, nb_vars, var)
    return temp


def supprimer_doublons(liste : ClauseBase) -> ClauseBase:
    liste_sans_doublons = []
    for sous_liste in liste:
        if sous_liste not in liste_sans_doublons:
            liste_sans_doublons.append(sous_liste)
    return liste_sans_doublons

def trouver_cle(dictionnaire, valeur):
    for cle, val in dictionnaire.items():
        if val == valeur:
            position  = cle[0],cle[1]
            return position
    return None
