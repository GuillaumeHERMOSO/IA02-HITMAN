from src.arbitre.hitman import *
from src.Class_HitmanKnowledge import *
from src.a_etoile import *

def trois_six(hr : HitmanReferee, know : HitmanKnowledge):
    status = hr.turn_clockwise()
    know.ajout_voir_knowledge(status)
    status = hr.turn_clockwise()
    know.ajout_voir_knowledge(status)
    status = hr.turn_clockwise()
    know.ajout_voir_knowledge(status)
    status = hr.turn_clockwise()
    know.ajout_voir_knowledge(status)
    #print(know)
    #print(status["position"])
    return status

def orientation_hitman(status :Dict):
    orientation :HC  = status["orientation"]
    if orientation == HC.N:
        offset = 0, 1
    elif orientation == HC.E:
        offset = 1, 0
    elif orientation == HC.S:
        offset = 0, -1
    elif orientation == HC.W:
        offset = -1, 0
    return offset
def nbr_inconu_autour_hitman(x :int, y :int, know :HitmanKnowledge):
    """ Renvoie le nombre de case inconnu autour de la position x,y, hitman a une vision de porter 3"""
    nbr = 0
    #on regarde nord : (x,y+1), (x,y+2), (x,y+3)
    #on regarde est : (x+1,y), (x+2,y), (x+3,y)
    #on regarde sud : (x,y-1), (x,y-2), (x,y-3)
    #on regarde ouest : (x-1,y), (x-2,y), (x-3,y)
    for i in range(1,4):
        if (x,y+i) not in know.knowledge and y+i < know.n and y+i >= 0:
            nbr += 1
        if (x+i,y) not in know.knowledge and x+i < know.m and x+i >= 0:
            nbr += 1
        if (x,y-i) not in know.knowledge and y-i < know.n and y-i >= 0:
            nbr += 1
        if (x-i,y) not in know.knowledge and x-i < know.m and x-i >= 0:
            nbr += 1

    return nbr

def get_liste_case_inconnu_plus_proche_hitman(x :int, y :int,n: int, m:int, know :HitmanKnowledge) -> List[Tuple[int,int]]:
    """ Retourne la liste des cases inconnu les plus proche de hitman trier par le calcul de la distance de manhattan et le nombre de mur entre hitman et la case"""
    case = []
    walls = know.get_walls()

    for i in range(n):
        for j in range(m):
            if (i,j) not in know.knowledge:
                case.append((i,j))
    case.sort(key=lambda x: (abs(x[0]-x),abs(x[1]-y),nbr_wall_entre((x[0],x[1]),(x,y),walls)))
    return case

def get_action(pos1 :Tuple[int,int], pos2 :Tuple[int,int], orientation : HC, know :HitmanKnowledge, hr:HitmanReferee) -> Tuple[List[Callable[[],None]],HC]:
    """"Renvoie une liste d'action et l'orientation pour aller de pos1 a pos2
        action possible : 
        move
        turn_clockwise
        turn_anti_clockwise
    """
    actions = []
    base = orientation
    if orientation == HC.N:
        if pos1[0] == pos2[0]   and pos1[1]+1 == pos2[1] :
            actions.append(hr.move)
        elif pos1[0] == pos2[0]  and pos1[1]-1 == pos2[1] :
            actions.append(hr.turn_clockwise)
            actions.append(hr.turn_clockwise)
            orientation = HC.S
            actions.append(hr.move)
        elif pos1[0]+1 == pos2[0]  and pos1[1] == pos2[1] :
            actions.append(hr.turn_clockwise)
            orientation = HC.E
            actions.append(hr.move)
        elif pos1[0]-1 == pos2[0]  and pos1[1] == pos2[1] :
            actions.append(hr.turn_anti_clockwise)
            orientation = HC.W
            actions.append(hr.move)
    
    elif orientation == HC.E:
        if pos1[0] == pos2[0]   and pos1[1]+1 == pos2[1] :
            actions.append(hr.turn_anti_clockwise)
            orientation = HC.N
            actions.append(hr.move)
        elif pos1[0] == pos2[0]  and pos1[1]-1 == pos2[1] :
            actions.append(hr.turn_clockwise)
            orientation = HC.S
            actions.append(hr.move)
        elif pos1[0]+1 == pos2[0]  and pos1[1] == pos2[1] :
            actions.append(hr.move)
        elif pos1[0]-1 == pos2[0]  and pos1[1] == pos2[1] :
            actions.append(hr.turn_clockwise)
            actions.append(hr.turn_clockwise)
            orientation = HC.W
            actions.append(hr.move)

    elif orientation == HC.S:
        if pos1[0] == pos2[0]   and pos1[1]+1 == pos2[1] :
            actions.append(hr.turn_clockwise)
            actions.append(hr.turn_clockwise)
            orientation = HC.N
            actions.append(hr.move)
        elif pos1[0] == pos2[0]  and pos1[1]-1 == pos2[1] :
            actions.append(hr.move)
        elif pos1[0]+1 == pos2[0]  and pos1[1] == pos2[1] :
            actions.append(hr.turn_anti_clockwise)
            orientation = HC.E
            actions.append(hr.move)
        elif pos1[0]-1 == pos2[0]  and pos1[1] == pos2[1] :
            actions.append(hr.turn_clockwise)
            orientation = HC.W
            actions.append(hr.move)

    elif orientation == HC.W:
        if pos1[0] == pos2[0]   and pos1[1]+1 == pos2[1] :
            actions.append(hr.turn_clockwise)
            orientation = HC.N
            actions.append(hr.move)
        elif pos1[0] == pos2[0]  and pos1[1]-1 == pos2[1] :
            actions.append(hr.turn_anti_clockwise)
            orientation = HC.S
            actions.append(hr.move)
        elif pos1[0]+1 == pos2[0]  and pos1[1] == pos2[1] :
            actions.append(hr.turn_clockwise)
            actions.append(hr.turn_clockwise)
            orientation = HC.E
            actions.append(hr.move)
        elif pos1[0]-1 == pos2[0]  and pos1[1] == pos2[1] :
            actions.append(hr.move)


    #print(f"on est en {pos1} et on va en {pos2} avec {base} et on fait {[x.__name__ for x in actions]}")
    return actions, orientation
    
def chemin_to_action(chemin :List[Tuple[int,int]], orientation_depart : HC, know :HitmanKnowledge, hr:HitmanReferee) -> List[Callable[[],None]]:
    """ Renvoie une liste d'action a partir d'un chemin"""
    actions = []
    o = orientation_depart
    for i in range(len(chemin)-1):
        a, o=get_action(chemin[i],chemin[i+1],o,know,hr)
        actions += a
    return actions

def affichage_liste_action(actions :List[Callable[[],None]]) -> None:
    """ Affiche les actions"""
    for a in actions:
        print(a.__name__)
    pass