from src.arbitre.hitman import *
from src.clause_dynamique import *
from src.clause_verite_sur_le_monde import *
from src.Class_HitmanKnowledge import *


def main():
    Knowledge = HitmanKnowledge(4,4)
    print(Knowledge)
    Knowledge.add_knowledge((0,0),HC.GUARD_N)
    print(Knowledge)
    Knowledge.add_knowledge((1,1),HC.SUIT)
    print(Knowledge)


    hr = HitmanReferee()
    status = hr.start_phase1()
    pprint(status)

    n = status["n"]
    m = status["m"]

    nbr_P = status["civil_count"] + status["guard_count"]

    list_var = creer_list_var(m,n)
    dict_var_to_num = creer_dictionnaire_cases_par_list(list_var)
    V_sur_le_monde : ClauseBase = []
    V_sur_le_monde += exactly_k(nbr_P,gen_var_lettre(m,n,dict_var_to_num,"P"))
    print(len(V_sur_le_monde))
    
    # TODO c'est long
    #dimac = clauses_to_dimacs(V_sur_le_monde,len(list_var))
    #write_dimacs_file(dimac, "./test.cnf")
    
    # TODO Mieux mais pas encore rapide
    # write_dimacs_file2(clauses = V_sur_le_monde, nb_vars = len(list_var), filename = "./test2.cnf")
    
    
    res = exec_gophersat( "test2.cnf")
    print(res)


    pass

if __name__ == "__main__":
    main()