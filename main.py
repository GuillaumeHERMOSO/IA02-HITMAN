import os
import random
from typing import List, Tuple
from src.arbitre.hitman import *
from src.clause_dynamique import *
from src.clause_verite_sur_le_monde import *
from src.Class_HitmanKnowledge import *

class HC(Enum): 
    EMPTY = 1
    WALL = 2
    GUARD_N = 3
    GUARD_E = 4
    GUARD_S = 5
    GUARD_W = 6
    CIVIL_N = 7
    CIVIL_E = 8
    CIVIL_S = 9
    CIVIL_W = 10
    TARGET = 11
    SUIT = 12
    PIANO_WIRE = 13
    N = 14
    E = 15
    S = 16
    W = 17


def trois_six(hr : HitmanReferee, know : HitmanKnowledge):
    status = hr.turn_clockwise()
    know.ajout_voir_knowledge(status)
    status = hr.turn_clockwise()
    know.ajout_voir_knowledge(status)
    status = hr.turn_clockwise()
    know.ajout_voir_knowledge(status)
    status = hr.turn_clockwise()
    know.ajout_voir_knowledge(status)
    print(know)
    print(status["position"])
    pass

def orientation_hitman(status :Dict):
    orientation :HC  = status["orientation"]
    if orientation.name == HC.N.name:
        offset = 0, 1
    elif orientation.name is HC.E.name:
        offset = 1, 0
    elif orientation.name is HC.S.name:
        offset = 0, -1
    elif orientation.name is HC.W.name:
        offset = -1, 0
    return offset


def main():
    
    """
    nbr_P = status["civil_count"] + status["guard_count"]
    list_var = creer_list_var(m,n)
    dict_var_to_num = creer_dictionnaire_cases_par_list(list_var)
    V_sur_le_monde : ClauseBase = []
    V_sur_le_monde += exactly_k(nbr_P,gen_var_lettre(m,n,dict_var_to_num,"P"))
    
    #print(len(V_sur_le_monde))
    
    # TODO c'est long
    #dimac = clauses_to_dimacs(V_sur_le_monde,len(list_var))
    #write_dimacs_file(dimac, "./test.cnf")
    
    # TODO Mieux mais pas encore rapide
    # write_dimacs_file2(clauses = V_sur_le_monde, nb_vars = len(list_var), filename = "./test2.cnf")
    
     
    res = exec_gophersat("test2.cnf")
    print(res)

    #TODO ne marche pas 
    #test_deduction("test2.cnf", 1)

    list_var = creer_list_var(m,n)
    dict_var_to_num = creer_dictionnaire_cases_par_list(list_var)

    pprint(Knowledge.get_all_knowledge())
    r = knowledge_to_clause_personne(Knowledge.get_all_knowledge(),dict_var_to_num)
    print(r)
    
    """  
    hr = HitmanReferee()
    status = hr.start_phase1()
    pprint(status)

    
    n = status["n"]
    m = status["m"]
    Knowledge = HitmanKnowledge(m,n)
    list_var = creer_list_var(m,n)
    dict_var_to_num = creer_dictionnaire_cases_par_list(list_var)

    #TODO attention mal coder on peut quitter la map

    #test mouvement random
    while (Knowledge.je_sais_pas_tt()):
        
        x,y = status["position"]
        off = orientation_hitman(status)
        x,y = x+off[0],y+off[1]
        random_move_list = []
        #on ajoute les fonction :
        if x >= 0 and x<=m and y >= 0 and y<=n:
            random_move_list.append(hr.move)
        random_move_list.append(hr.turn_anti_clockwise)
        random_move_list.append(hr.turn_clockwise)

        #on choisit une fonction random
        random_move = random.choice(random_move_list)
        #on execute la fonction
        status = random_move()
        #on ajoute le knowledge
        Knowledge.ajout_voir_knowledge(status)
        #on efface la console et on affiche le knowledge
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Knowledge)
        print(status["position"],status["orientation"], status["penalties"])
    
    print(hr.send_content(Knowledge.get_all_knowledge()))



    pass


def main2() :
    hr = HitmanReferee()
    status = hr.start_phase1()
    n = status["n"]
    m = status["m"]
    nbr_P = status["civil_count"] + status["guard_count"]
    list_var = creer_list_var(m, n)
    dict_var_to_num = creer_dictionnaire_cases_par_list(list_var)
    V_sur_le_monde: ClauseBase = []
    V_sur_le_monde += exactly_k(nbr_P, gen_var_lettre(m, n, dict_var_to_num, "P"))
    write_dimacs_file2(clauses=V_sur_le_monde, nb_vars=len(list_var), filename="./test2.cnf")
    res = exec_gophersat("test2.cnf")
    print(res)
    # test_deduction("C:\\Users\\jawed\\Documents\\GitHub\\IA02-HITMAN\\test2.cnf", 1)


if __name__ == "__main__":
    #main2()
    main()