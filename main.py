from src.arbitre.hitman import *
from src.clause_dynamique import *
from src.clause_verite_sur_le_monde import *
from src.Class_HitmanKnowledge import *


def main():
    

    hr = HitmanReferee()
    status = hr.start_phase1()
    pprint(status)

    n = status["n"]
    m = status["m"]

    Knowledge = HitmanKnowledge(m,n)

    Knowledge.add_knowledge((0,0),HC.GUARD_N)
    print(Knowledge)
    print()
    Knowledge.affichage_vison()


    Knowledge.add_knowledge((0,5),HC.GUARD_S)
    print(Knowledge)
    print()
    Knowledge.affichage_vison()

    Knowledge.add_knowledge((0,1),HC.PIANO_WIRE)
    print(Knowledge)
    print()
    Knowledge.affichage_vison()

    Knowledge.add_knowledge((0,0),HC.GUARD_N)


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
    
    """   
    res = exec_gophersat("test2.cnf")
    print(res)

    #TODO ne marche pas 
    #test_deduction("test2.cnf", 1)

    list_var = creer_list_var(m,n)
    dict_var_to_num = creer_dictionnaire_cases_par_list(list_var)

    pprint(Knowledge.get_all_knowledge())
    r = knowledge_to_clause_personne(Knowledge.get_all_knowledge(),dict_var_to_num)
    print(r)


    Knowledge = HitmanKnowledge(m,n)
    list_var = creer_list_var(m,n)
    dict_var_to_num = creer_dictionnaire_cases_par_list(list_var)

    status = hr.move()
    pprint(status)
    Knowledge.ajout_voir_knowledge(status, dict_var_to_num)
    print(Knowledge)
    pass

if __name__ == "__main__":
    main()