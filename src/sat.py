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
    list_cases = []
    for j in range(0,m):
        for i in range(0,n):
                list_cases.append("%d%d_%s"%(i,j,"P"))
    return list_cases

def creer_dictionnaire_cases_par_list(list_variable : list) -> Tuple[dict,int]:
    # Création du dictionnaire une variable = un chiffre:
    compteur = 0
    dict_cases = {}
    for var in list_variable:  # var = "ij_P"
        compteur += 1
        dict_cases[var] = compteur

    return dict_cases, compteur

def gen_var_lettre(m: int, n: int, dico_var_to_num: dict, lettre: str) -> list:
    list_var = []
    for i in range(0,m):
        for j in range(0,n):
            list_var.append(dico_var_to_num["%d%d_%s"%(i,j,lettre)])
    return list_var

def write_dimacs_file(dimacs: str, filename: str):
    with open(filename, "w", newline="") as cnf:
        cnf.write(dimacs)
def clauses_to_dimacs(clauses: ClauseBase, nb_vars: int) -> str:
    r = f"p cnf {nb_vars} {len(clauses)}\n"
    i=0
    for clause in clauses:
        for literal in clause:
            r += f"{literal} "
        r += "0\n"
        #affichage du numéro de clause
        print(i, end ="\r");i+=1
    return r

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

def add_list_to_set(seta: set, liste_a: List):
    for elt in liste_a:
        seta.add(elt)
    return seta



def test_deduction(filename: str, var_tester: int):
    # on ajoute la negation de la variable a tester dans le ficher
    try:
        with open(filename, 'r') as source:
            contenu = source.read()         #lecture du fichier
            temp = contenu
            lignes_contenu = contenu.split("\n")        # Séparation en ligne par ligne
            ligne_1 = lignes_contenu[0].split(" ")      # Séparation de la première ligne
            ligne_1[-1] = str(int(ligne_1[-1])+1)       # Incrémentation du nb de clauses
            lignes_contenu[0] = ' '.join(ligne_1)        # Sauvegarde de la ligne modifié
            lignes_contenu.append(f"-{var_tester} 0")      # Ajout de la nouvelle clause négative
            contenu = "\n".join(lignes_contenu)         # Retransformation du fichier

        with open(filename, "w", encoding="utf-8") as destination:
            destination.write(contenu)                      # Réecriture du fichier

        print("Le fichier a été dupliqué avec succès.")
    except FileNotFoundError:
        print("Le fichier source n'existe pas. Réessayez")
        return

    # Si c'est bon on lance gophersat
    res = exec_gophersat("test2.cnf")
    if res[0] == False:
        print(f"on deduit {var_tester}")
        lignes_contenu[-1] = f"{var_tester} 0"
        temp = "\n".join(lignes_contenu)         # Retransformation du fichier
    with open(filename, "w", encoding="utf-8") as destination:
        destination.write(temp)                      # Réecriture du fichier




def deduction(dict_var_to_num : dict,hc : HitmanKnowledge,Clauses : ClauseBase, nb_vars: int, var_tester: int):
    # on creer un fichier de clauses
    temp = Clauses +[[-var_tester]]
    write_dimacs_file2(temp, nb_vars, "sat.cnf")
    #on test la deduction
    res = exec_gophersat("sat.cnf")
    print("Deduction potentielle : ", end="")
    print(trouver_cle(dict_var_to_num, var_tester), end=" ")
    if res[0] == False:
        print(f"on deduit  : {trouver_cle(dict_var_to_num,var_tester)}")
        pos = trouver_cle(dict_var_to_num,var_tester) # On récupère les coordonnées de l'individu déduit
        hc.add_knowledge(pos,HC.N)   # Ajout d'un individu déduit
        return  Clauses +[[var_tester]]
    elif res[0] == True:
        print(f"on n'a pas pu déduire :  {trouver_cle(dict_var_to_num,var_tester)}")



    return Clauses

def boucle_deduction(dict_var_to_num : dict,hc : HitmanKnowledge,clauses : ClauseBase, nb : int) -> ClauseBase:
    temp = clauses
    list_var = []
    clauses_unitaires = []
    clauses_1D = transformer_en_liste_simple(clauses)
    if len(clauses_1D) < 60 :
        print(clauses)
        print("clauses 1D : ",clauses_1D)
    for ligne in clauses:
        if len(ligne) == 1:  # clause unitaire
            clauses_unitaires.append(ligne[0])
    for elt in clauses_1D :
        if -elt not in clauses_unitaires and elt not in clauses_unitaires :
            if elt not in list_var and elt>0:
                list_var.append(elt)  # On ne teste que des variables non-unitaires et deja dans les clauses : les ecoutes !
    if list_var == [] :
        print("On ne peut rien deduire pour le moment")
        return clauses # rien à deduire, tout est connu
    nb_vars = nb
    print("liste : ",list_var)
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

def transformer_en_liste_simple(liste):
    liste_simple = []
    for sous_liste in liste:
        liste_simple.extend(sous_liste)
    return liste_simple
