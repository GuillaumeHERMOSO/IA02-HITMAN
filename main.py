import os
import random
from typing import List, Tuple
from src.arbitre.hitman import *
from src.Class_HitmanKnowledge import *
from src.clause_verite_sur_le_monde import *
from src.arbitre.hitman import HC
from src.mouvement_phase1 import *
from src.a_etoile import *


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
    V_sur_le_monde: ClauseBase = set()
    add_list_to_set(V_sur_le_monde,exactly_k(nbr_P, gen_var_lettre(m, n, dict_var_to_num, "P")))
    write_dimacs_file2(clauses=V_sur_le_monde, nb_vars=len(list_var), filename="./test2.cnf")
    res = exec_gophersat("test2.cnf")
    print(res)

    test_deduction("test2.cnf", 1)


    # MARCHE SI LA CARTE EST CONNUE et complete
    complete_map_example = {
    (0, 5): HC.EMPTY,
    (1, 5): HC.EMPTY,
    (2, 5): HC.EMPTY,
    (3, 5): HC.SUIT,
    (4, 5): HC.GUARD_S,
    (5, 5): HC.WALL,
    (6, 5): HC.WALL,
    (0, 4): HC.EMPTY,
    (1, 4): HC.WALL,
    (2, 4): HC.EMPTY,
    (3, 4): HC.EMPTY,
    (4, 4): HC.EMPTY,
    (5, 4): HC.EMPTY,
    (6, 4): HC.EMPTY,
    (0, 3): HC.TARGET,
    (1, 3): HC.WALL,
    (2, 3): HC.EMPTY,
    (3, 3): HC.EMPTY,
    (4, 3): HC.EMPTY,
    (5, 3): HC.CIVIL_N,
    (6, 3): HC.EMPTY,
    (0, 2): HC.WALL,
    (1, 2): HC.WALL,
    (2, 2): HC.EMPTY,
    (3, 2): HC.GUARD_E,
    (4, 2): HC.EMPTY,
    (5, 2): HC.CIVIL_E,
    (6, 2): HC.CIVIL_W,
    (0, 1): HC.EMPTY,
    (1, 1): HC.EMPTY,
    (2, 1): HC.EMPTY,
    (3, 1): HC.EMPTY,
    (4, 1): HC.EMPTY,
    (5, 1): HC.EMPTY,
    (6, 1): HC.EMPTY,
    (0, 0): HC.EMPTY,
    (1, 0): HC.EMPTY,
    (2, 0): HC.WALL,
    (3, 0): HC.WALL,
    (4, 0): HC.EMPTY,
    (5, 0): HC.PIANO_WIRE,
    (6, 0): HC.EMPTY,
    }
    m = 6
    n = 7
    con = HitmanKnowledge(m=m, n=n)
    con.knowledge = complete_map_example
    print(con)

    walls = con.get_liste_mur()
    case_vu = con.get_liste_casevu()


    print("Début de l'algo")
    s0 = (0,0)
    goal = (6,4)

    s, d = astar_with_parent(s0, goal, succ, con.get_all_knowledge(),m,n, walls, case_vu)
    print("Fin de l'algo")
    print("Début de la reconstruction du chemin")
    chemin = []
    while s != s0:
        chemin.append(s)
        s = d[s]
    chemin.append(s0)
    chemin.reverse()
    print("Fin de la reconstruction du chemin")
    print(chemin)
    #def chemin_to_action(chemin :List[Tuple[int,int]], orientation_depart : HC, know :HitmanKnowledge, hr:HitmanReferee) -> List[Callable[[],None]]:

    hr =HitmanReferee()
    status = hr.start_phase1()
    o = status["orientation"]

    actions = chemin_to_action(chemin, o, con, hr)
    #print(actions)
    #affichage_liste_action(actions)
    for a in actions:
        status = a()
        print(status["position"],status["orientation"], status["penalties"])
    print(o)

def main5():
    # Debut de phase 1
    hr = HitmanReferee()
    status = hr.start_phase1()
    n = status["n"]
    m = status["m"]
    con = HitmanKnowledge(m=m, n=n)
    con.ajout_voir_knowledge(status)
    afficher(con,hr)
    
    input("Appuyer sur une touche pour continuer")
    status = debut_map(hr,con)
    os.system('cls' if os.name == 'nt' else 'clear')
    afficher(con,hr)
    print(status["position"],status["orientation"], status["penalties"])
    s0 = status["position"]
    visited = [s0]

    while (con.je_sais_pas_tt()):
        # Tant que Hitman c'est pas tout 
        s0 = status["position"]
        visited.append(s0)

        #on regarde les cases inconnus les plus proches
        liste = get_liste_case_inconnu_plus_proche_hitman(s0[0],s0[1], n,m, con)
        test = []
        
        while test == []:
            #on prend la premiere case de la liste
            goal = liste.pop(0)
            print(f"on est en {status['position']} on veut voir {goal}")
            #on regarde ou on peut aller pour voir la case
            test, orientation_a_obtenir = case_connu_qui_peut_voir_une_case(goal, m, n, con.get_all_knowledge())
            print (f" on va donc en : {test}")

        s, d = astar_with_parent(s0, test, succ, con.get_all_knowledge(),m,n, con.get_liste_mur(), con.get_liste_casevu(), visited)
        oro = orientation_a_obtenir[s]
        
        print(f"s = {s}")
        chemin = []
        while s != s0:
            chemin.append(s)
            s = d[s]
        chemin.append(s0)
        chemin.reverse()
        
        print(f"Le chemin est : {chemin}")
        orientation= status["orientation"]
        # on transforme le chemin en liste d'action qu'on execute
        actions = chemin_to_action(chemin, orientation, con, hr)
        print(f"on fait donc les actions : {actions}")
        input("Appuyer sur une touche pour continuer")
        for a in actions:
            status = a()
            con.ajout_voir_knowledge(status)
            os.system('cls' if os.name == 'nt' else 'clear')
            afficher(con, hr)
            sleep(0.2)
        os.system('cls' if os.name == 'nt' else 'clear')
        afficher(con, hr)
        print(status["position"],status["orientation"], status["penalties"])

        #on est au bon endroit on tourne dans la direction nous permettant de voir la case inconnu        
        tourner_action = tourner( status["orientation"],oro, hr)
        print(f" on est en a la case {status['position']} avec l'orientation {status['orientation']} et on veut tourner en {oro}")
        for a in tourner_action:
            print(a.__name__)
            status = a()
            con.ajout_voir_knowledge(status)
        
        con.affichage_vison()
        print("\n _____________________________________________________________________________________________\n")
        os.system('cls' if os.name == 'nt' else 'clear')
        afficher(con, hr)
        print(status["position"],status["orientation"], status["penalties"])
        print("fin du tour\n\n\n\n")
        input("Appuyer sur une touche pour continuer")

  

    # on a tout vu on envoie le contenu
    print(hr.send_content(con.get_all_knowledge()))
    status = hr.end_phase1()
    print(status[1])


    pass


if __name__ == "__main__":
    main5()
    #main2()