import os
import random
from typing import List, Tuple
from src.arbitre.hitman import *
from src.clause_dynamique import *
from src.clause_verite_sur_le_monde import *
from src.Class_HitmanKnowledge import *
from src.arbitre.hitman import HC
from src.mouvement_phase1 import *
from src.test_mouvement import *


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
    
    # TODO Mieux mais pas encore rapide (Toi 5MIN --> Moi 1min )
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
    Knowledge.ajout_voir_knowledge(status)
    """    
    list_var = creer_list_var(m,n)
    dict_var_to_num = creer_dictionnaire_cases_par_list(list_var)

    Knowledge.ajout_voir_knowledge(status)
    print(Knowledge)
    print(case_inconnu_plus_proche_hitman(0,2,n,m,Knowledge))
    sleep(5)
    """


    #TODO attention mal coder on peut quitter la map

    #test mouvement random
    while (Knowledge.je_sais_pas_tt()):
        
        x,y = status["position"]
        off = orientation_hitman(status)
        x,y = x+off[0],y+off[1]
        random_move_list = []
        #on ajoute les fonction :
        if x >= 0 and x<=m and y >= 0 and y<=n :
            if Knowledge.has_knowledge(x,y) == False:
                random_move_list.append(hr.move)
            elif Knowledge.knowledge[(x,y)] not in [HC.GUARD_E,HC.GUARD_N,HC.GUARD_S,HC.GUARD_W] or status["is_in_guard_range"]:
                random_move_list.append(hr.move)
        random_move_list.append(hr.turn_anti_clockwise)
        random_move_list.append(hr.turn_clockwise)

        #on choisit une fonction random
        random_move = random.choice(random_move_list)
        #on execute la fonction
        status = random_move()
        #on ajoute le knowledge
        Knowledge.ajout_voir_knowledge(status)
        #print(Knowledge.get_all_knowledge())
        #on efface la console et on affiche le knowledge
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Knowledge, "\n\n")
        print(status["position"],status["orientation"], status["penalties"])
    
    print(hr.send_content(Knowledge.get_all_knowledge()))
    Knowledge.affichage_vison()
    print(f"m = {m} n = {n}")



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

    test_deduction("test2.cnf", 1)

def main3():
    hr = HitmanReferee()
    status = hr.start_phase1()
    n = status["n"]
    m = status["m"]
    Knowledge = HitmanKnowledge(m,n)
    coller_bordure(n , m , hr , Knowledge )
    pass

if __name__ == "__main__":
    main3()
    #main2()