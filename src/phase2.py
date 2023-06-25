import os
from src.mouvement_phase1 import *
from src.a_etoile import *
from src.arbitre.hitman import *
from src.Class_HitmanKnowledge import *
from pprint import pprint
from time import sleep



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

def get_case_suit(con : HitmanKnowledge):
    for pos,val in con.knowledge.items():
        if val == HC.SUIT:
            return pos
    return None


def deplacement(s0, s, d, orientation, con, hr):
    chemin = []
    while s != s0:
        chemin.append(s)
        s = d[s]
    chemin.append(s0)
    chemin.reverse()
    actions = chemin_to_action(chemin, orientation, con, hr)
    return actions

def consequence_action(hr,a,pos,orientation):
    if a == hr.move:
        if orientation == HC.N:
            return (pos[0],pos[1]+1), orientation
        if orientation == HC.S:
            return (pos[0],pos[1]-1), orientation
        if orientation == HC.E:
            return (pos[0]+1,pos[1]), orientation
        if orientation == HC.W:
            return (pos[0]-1,pos[1]), orientation
    if a == hr.turn_clockwise:
        if orientation == HC.N:
            return pos, HC.E
        if orientation == HC.S:
            return pos, HC.W
        if orientation == HC.E:
            return pos, HC.S
        if orientation == HC.W:
            return pos, HC.N
    if a == hr.turn_anti_clockwise:
        if orientation == HC.N:
            return pos, HC.W
        if orientation == HC.S:
            return pos, HC.E
        if orientation == HC.E:
            return pos, HC.N
        if orientation == HC.W:
            return pos, HC.S
    else:
        return pos, orientation

def coup_action(hr : HitmanReferee,a,pos,orientation,connaissance : HitmanKnowledge):
    s = 0
    if a in [hr.move, hr.turn_clockwise, hr.turn_anti_clockwise,  hr.take_suit, hr.take_weapon]:
        s += 1
        print(f"pos : {pos}, action : {a.__name__}")
        if pos in connaissance.get_liste_casevu() or pos in connaissance.get_liste_casevu_civil():
            s +=5
    if a in [hr.neutralize_civil, hr.neutralize_guard, hr.kill_target]:
        s+= 20
        if pos in connaissance.get_liste_casevu() or pos in connaissance.get_liste_casevu_civil():
            s +=100
    if a == hr.put_on_suit:
        s +=1
        if pos in connaissance.get_liste_casevu() or pos in connaissance.get_liste_casevu_civil():
            s +=100
    return s   

def orientation_chemin(list_actions : List, pos_depart, orientation_depart, hr):
    pos = pos_depart
    orientation = orientation_depart
    for a in list_actions:
        pos, orientation = consequence_action(hr,a,pos,orientation)
    return orientation

def coup_chemin (list_actions : List, pos_depart, orientation_depart, connaissance: HitmanKnowledge,hr):
    s = 0
    pos = pos_depart
    orientation = orientation_depart
    for a in list_actions:
        s += coup_action(hr,a,pos,orientation,connaissance)
        pos, orientation = consequence_action(hr,a,pos,orientation)
    return s

def coup_chemin2(list_actions :List, hr: HitmanReferee):
    temp = deepcopy(hr)
    temp.start_phase2()
    for a in list_actions:
        if a == hr.move:
            temp.move()
        if a == hr.turn_clockwise:
            temp.turn_clockwise()
        if a == hr.turn_anti_clockwise:
            temp.turn_anti_clockwise()
        if a == hr.take_suit:
            temp.take_suit()
        if a == hr.take_weapon:
            temp.take_weapon()
        if a == hr.put_on_suit:
            temp.put_on_suit()
        if a == hr.neutralize_civil:
            temp.neutralize_civil()
        if a == hr.neutralize_guard:
            temp.neutralize_guard()
        if a == hr.kill_target:
            temp.kill_target()
    status = temp.end_phase2()
    # on a status[1] = 'Your score is -48' on souhaite récupérer le -48
    score = int(status[1].split(' ')[-1])
    del temp
    return score





def phase2(hr: HitmanReferee, con : HitmanKnowledge, affichage = False, temp = 0.5):
    visited = []
    status = hr.start_phase2()
    n = status["n"]
    m = status["m"]
    s0 = status["position"]
    orientation = status["orientation"]
    orientation_dep = orientation
    s0_dep = s0

    # actions 1 : depart -> corde -> target -> tuer -> 0,0   
    actions_1 = []

        #deplacement vers la corde
    s0 = s0_dep
    orientation = orientation_dep
    but = [get_case_piano(con)]
    s, d = astar_with_parent(s0, but, succ, con.get_all_knowledge(),m,n, con.get_liste_mur(), con.get_liste_casevu(), visited)

    actions = deplacement(s0, s, d, orientation, con, hr)
    actions_1 += actions
    orientation= orientation_chemin(actions_1, s0_dep, orientation_dep,hr)
        #on est a la corde, on la prend
    actions_1.append(hr.take_weapon)

        #deplacement vers la target
    s0 = but[0]
    but = [get_case_target(con)]
    s, d = astar_with_parent(s0, but, succ, con.get_all_knowledge(),m,n, con.get_liste_mur(), con.get_liste_casevu(), visited)
    
    actions = deplacement(s0, s, d, orientation, con, hr)    
    actions_1 += actions
    orientation= orientation_chemin(actions_1, s0_dep, orientation_dep,hr)
    
        #on est a la target, on la tue
    actions_1.append(hr.kill_target)

        #deplacement vers 0,0
    s0 = but[0]
    but = [(0,0)]
    s, d = astar_with_parent(s0, but, succ, con.get_all_knowledge(),m,n, con.get_liste_mur(), con.get_liste_casevu(), visited)
    actions = deplacement(s0, s, d, orientation, con, hr)
    actions_1 += actions
    orientation= orientation_chemin(actions_1, s0_dep, orientation_dep,hr)
    if affichage:
        print(f"actions 1 : {coup_chemin2(actions_1,hr)}")




    #actions 2 : depart -> costume -> corde -> target -> tuer -> 0,0
    actions_2 = []
        #deplacement vers le costume
    s0 = s0_dep
    orientation = orientation_dep
    but = [get_case_suit(con)]
    s, d = astar_with_parent(s0, but, succ, con.get_all_knowledge(),m,n, con.get_liste_mur(), con.get_liste_casevu(), visited)
    actions = deplacement(s0, s, d, orientation, con, hr)
    actions_2 += actions
    orientation= orientation_chemin(actions_2, s0_dep, orientation_dep,hr)

        #on est au costume, on le prend et on le met
    actions_2+= [hr.take_suit,hr.put_on_suit]

        #deplacement vers la corde
    s0 = but[0]
    but = [get_case_piano(con)]
    s, d = astar_with_parent(s0, but, succ, con.get_all_knowledge(),m,n, con.get_liste_mur(), con.get_liste_casevu(), visited,True)
    actions = deplacement(s0, s, d, orientation, con, hr)
    actions_2 += actions
    orientation= orientation_chemin(actions_2, s0_dep, orientation_dep,hr)

        #on est a la corde, on la prend
    actions_2.append(hr.take_weapon)

        #deplacement vers la target
    s0 = but[0]
    but = [get_case_target(con)]
    s, d = astar_with_parent(s0, but, succ, con.get_all_knowledge(),m,n, con.get_liste_mur(), con.get_liste_casevu(), visited,True)
    actions = deplacement(s0, s, d, orientation, con, hr)
    actions_2 += actions
    orientation= orientation_chemin(actions_2, s0_dep, orientation_dep,hr)

        #on est a la target, on la tue
    actions_2.append(hr.kill_target)
    
        #deplacement vers 0,0
    s0 = but[0]
    but = [(0,0)]
    s, d = astar_with_parent(s0, but, succ, con.get_all_knowledge(),m,n, con.get_liste_mur(), con.get_liste_casevu(), visited,True)
    actions = deplacement(s0, s, d, orientation, con, hr)
    actions_2 += actions
    orientation= orientation_chemin(actions_2, s0_dep, orientation_dep,hr)
    if affichage:
        print(f"actions 2 : {coup_chemin2(actions_2,hr)}")
    
    

    #actions 3 : depart -> corde -> costume -> target -> tuer -> 0,0
    actions_3 = []

        #deplacement vers la corde
    s0 = s0_dep
    orientation = orientation_dep
    but = [get_case_piano(con)]
    s, d = astar_with_parent(s0, but, succ, con.get_all_knowledge(),m,n, con.get_liste_mur(), con.get_liste_casevu(), visited)
    actions = deplacement(s0, s, d, orientation, con, hr)
    actions_3 += actions
    orientation= orientation_chemin(actions_3, s0_dep, orientation_dep,hr)

        #on est a la corde, on la prend
    actions_3.append(hr.take_weapon)

        #deplacement vers le costume
    s0 = but[0]
    but = [get_case_suit(con)]
    s, d = astar_with_parent(s0, but, succ, con.get_all_knowledge(),m,n, con.get_liste_mur(), con.get_liste_casevu(), visited)
    actions = deplacement(s0, s, d, orientation, con, hr)
    actions_3 += actions
    orientation= orientation_chemin(actions_3, s0_dep, orientation_dep,hr)

        #on est au costume, on le prend et on le met
    actions_3+= [hr.take_suit,hr.put_on_suit]

        #deplacement vers la target
    s0 = but[0]
    but = [get_case_target(con)]
    s, d = astar_with_parent(s0, but, succ, con.get_all_knowledge(),m,n, con.get_liste_mur(), con.get_liste_casevu(), visited,True)
    actions = deplacement(s0, s, d, orientation, con, hr)
    actions_3 += actions
    orientation= orientation_chemin(actions_3, s0_dep, orientation_dep,hr)

        #on est a la target, on la tue
    actions_3.append(hr.kill_target)

        #deplacement vers 0,0
    s0 = but[0]
    but = [(0,0)]
    s, d = astar_with_parent(s0, but, succ, con.get_all_knowledge(),m,n, con.get_liste_mur(), con.get_liste_casevu(), visited,True)
    actions = deplacement(s0, s, d, orientation, con, hr)
    actions_3 += actions
    orientation= orientation_chemin(actions_3, s0_dep, orientation_dep,hr)

    if affichage:
        print(f"actions 3 : {coup_chemin2(actions_3,hr)}")
        sleep(3*temp)




    #on prend le chemin le moins coûteux en fct de coup_chemin2
    min_actions = actions_1

    if abs(coup_chemin2(actions_2,hr)) < abs(coup_chemin2(min_actions,hr)):
        min_actions = actions_2
    if abs(coup_chemin2(actions_3,hr)) < abs(coup_chemin2(min_actions,hr)):
        min_actions = actions_3

    

    for a in min_actions: 
        status = a()
        if affichage:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(a.__name__)
            afficher(con, hr,status)
            print(f"{status['position']} {status['orientation']} p :{status['penalties']}")

            sleep(temp)


    status=hr.end_phase2()
    pprint(status)

