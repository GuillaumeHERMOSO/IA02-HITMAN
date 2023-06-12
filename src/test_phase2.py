from src.mouvement_phase1 import *
from src.a_etoile import *
from src.arbitre.hitman import *
from src.Class_HitmanKnowledge import *
from pprint import pprint
def get_case_piano(con : HitmanKnowledge):
    for pos,val in con.knowledge.items():
        if val == HC.PIANO_WIRE:
            return pos
    return None

def get_case_target(con : HitmanKnowledge):
    for pos,val in con.knowledge.items():
        if val == HC.TARGET:
            return pos
    return None

def test_phase2(hr: HitmanReferee, con : HitmanKnowledge, visited : List[Tuple[int,int]]):
    status = hr.start_phase2()
    #pprint(status)
    
    n = status["n"]
    m = status["m"]

    but = [get_case_piano(con)]
    s0 = status["position"]
    print(con)
    print(f"on est en {s0} et on veut aller en {but[0]}")
    s, d = astar_with_parent(s0, but, succ, con.get_all_knowledge(),m,n, con.get_liste_mur(), con.get_liste_casevu(), visited)
    chemin = []
    #TODO faire une fct
    while s != s0:
        chemin.append(s)
        s = d[s]
    chemin.append(s0)
    chemin.reverse()
    
    print(f"Le chemin est : {chemin}")
    orientation= status["orientation"]
    actions = chemin_to_action(chemin, orientation, con, hr)
    for a in actions:
        status = a()
        con.ajout_voir_knowledge(status)
    print(status["position"],status["orientation"], status["penalties"])

    #on est a la corde, on la prend
    status = hr.take_weapon()


    but = [get_case_target(con)]
    s0 = status["position"]
    s, d = astar_with_parent(s0, but, succ, con.get_all_knowledge(),m,n, con.get_liste_mur(), con.get_liste_casevu(), visited)
    chemin = []
    #TODO faire une fct
    while s != s0:
        chemin.append(s)
        s = d[s]
    chemin.append(s0)
    chemin.reverse()
    
    print(f"Le chemin est : {chemin}")
    orientation= status["orientation"]
    actions = chemin_to_action(chemin, orientation, con, hr)
    for a in actions:
        status = a()
        con.ajout_voir_knowledge(status)
    print(status["position"],status["orientation"], status["penalties"])

    status = hr.kill_target()

    but = [(0,0)]
    s0 = status["position"]
    s, d = astar_with_parent(s0, but, succ, con.get_all_knowledge(),m,n, con.get_liste_mur(), con.get_liste_casevu(), visited)
    chemin = []
    #TODO faire une fct
    while s != s0:
        chemin.append(s)
        s = d[s]
    chemin.append(s0)
    chemin.reverse()
    
    print(f"Le chemin est : {chemin}")
    orientation= status["orientation"]
    actions = chemin_to_action(chemin, orientation, con, hr)
    for a in actions:
        status = a()
        con.ajout_voir_knowledge(status)
    print(status["position"],status["orientation"], status["penalties"])

    status=hr.end_phase2()
    pprint(status)
    print(status[0])
