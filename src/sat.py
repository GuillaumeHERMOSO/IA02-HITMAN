from typing import List, Dict, Tuple
import subprocess
Grid = List[List[int]]
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]
Model = List[Literal]

def creer_list_var(m: int, n: int) -> list:
    list_cases = []
    for i in range(0,m):
        for j in range(0,n):
                list_cases.append("%d%d_%s"%(i,j,"P"))
    return list_cases

def creer_dictionnaire_cases_par_list(list_variable : list) -> dict:
    # Création du dictionnaire une variable = un chiffre:
    compteur = 1
    dict_cases = {}
    for i in list_variable:
        dict_cases[i] = compteur
        compteur += 1
    return dict_cases

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


def test_deduction(filename: str, var_tester: int):
    # on ajoute la negation de la variable a tester dans un ficher temporaire
    try:
        with open(filename, 'r') as source:
            with open("temp.cnf", 'w') as destination:
                destination.write(source.read())
        print("Le fichier a été dupliqué avec succès.")
    except FileNotFoundError:
        print("Le fichier source n'existe pas.")
    with open("temp.cnf", "a") as cnf:
        cnf.write(f"-{var_tester} 0")
    # on lance gophersat
    res = exec_gophersat("temp.cnf")
    if res[0] == False:
        print(f"on deduit {var_tester}")
        return var_tester
    else:
        return None

    
