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
    walls = know.get_liste_mur()

    for i in range(n):
        for j in range(m):
            if (i,j) not in know.knowledge or  know.knowledge[(i,j)] in [HC.N, HC.E, HC.S, HC.W]:
                case.append((i,j))
    case.sort(key=lambda k: (distanceManhattan(k,(x,y))))
    #print(case)
    #TODO trier     case.sort(key=lambda k: (distanceManhattan(k,(x,y)) + 5* nbr_wall_entre((x[0],x[1]),(x,y),walls)))

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

def tourner(orientation_actuel: HC, orientation_voulu: HC, hr:HitmanReferee) -> List[Callable[[],None]]:
    """ Renvoie une liste d'action pour tourner de orientation_actuel a orientation_voulu"""
    if orientation_actuel == orientation_voulu:
        return []
    if orientation_actuel == HC.N:
        if orientation_voulu == HC.E:
            return [hr.turn_clockwise]
        elif orientation_voulu == HC.S:
            return [hr.turn_clockwise,hr.turn_clockwise]
        elif orientation_voulu == HC.W:
            return [hr.turn_anti_clockwise]
    elif orientation_actuel == HC.E:
        if orientation_voulu == HC.S:
            return [hr.turn_clockwise]
        elif orientation_voulu == HC.W:
            return [hr.turn_clockwise,hr.turn_clockwise]
        elif orientation_voulu == HC.N:
            return [hr.turn_anti_clockwise]
    elif orientation_actuel == HC.S:
        if orientation_voulu == HC.W:
            return [hr.turn_clockwise]
        elif orientation_voulu == HC.N:
            return [hr.turn_clockwise,hr.turn_clockwise]
        elif orientation_voulu == HC.E:
            return [hr.turn_anti_clockwise]
    elif orientation_actuel == HC.W:
        if orientation_voulu == HC.N:
            return [hr.turn_clockwise]
        elif orientation_voulu == HC.E:
            return [hr.turn_clockwise,hr.turn_clockwise]
        elif orientation_voulu == HC.S:
            return [hr.turn_anti_clockwise]
        

def debut_map(hr : HitmanReferee, know : HitmanKnowledge):
    status = hr.start_phase1()
    pos = status["position"]
    orientation = status["orientation"]
    n = status["n"]
    m = status["m"]
    know.ajout_voir_knowledge(status)
    # une position est un tuple (x,y), x dans 0 a n-1 et y dans 0 a m-1
    # On regarde ce qu'il y a autour de nous mais pas la bordure de la map
    bordure_N = [(x,m-1) for x in range(0,n-1)]
    bordure_E = [(n-1,y) for y in range(0,m-1)]
    bordure_S = [(x,0) for x in range(0,n-1)]
    bordure_W = [(0,y) for y in range(0,m-1)]

    # si on est dans un angle on regarde les deux cotes
    if pos == (0,0):
        # on doit regarder a l'est et au nord
        if orientation == HC.N:
            #on connait deja le nord
            #on regarde a l'est 
            status = hr.turn_clockwise()
            know.ajout_voir_knowledge(status)
        elif orientation == HC.W:
            #on regarde au nord
            status = hr.turn_clockwise()
            know.ajout_voir_knowledge(status)
            #on regarde a l'est
            status = hr.turn_clockwise()
            know.ajout_voir_knowledge(status)
        elif orientation == HC.S:
            #on regarde a l'est
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
            #on regarde au nord
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
        elif orientation == HC.E:
            #on regarde au nord
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
    elif pos == (n-1,0):
        # on doit regarder a l'ouest et au nord
        if orientation == HC.N:
            #on regarde a l'ouest
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
        elif orientation == HC.E:
            #on regarde au nord
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
            #on regarde a l'ouest
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
        elif orientation == HC.S:
            #on regarde a l'ouest
            status = hr.turn_clockwise()
            know.ajout_voir_knowledge(status)
            #on regarde au nord
            status = hr.turn_clockwise()
            know.ajout_voir_knowledge(status)
        elif orientation == HC.W:
            #on regarde au nord
            status = hr.turn_clockwise()
            know.ajout_voir_knowledge(status)
    elif pos == (n-1,m-1):
        # on doit regarder a l'ouest et au sud
        if orientation == HC.S:
            #on regarde a l'ouest
            status = hr.turn_clockwise()
            know.ajout_voir_knowledge(status)
        elif orientation == HC.W:
            #on regarde au sud
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)

        elif orientation == HC.N:
            #on regarde a l'ouest
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
            #on regarde au sud
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
        elif orientation == HC.E:
            #on regarde au sud
            status = hr.turn_clockwise()
            know.ajout_voir_knowledge(status)
            #on regarde a l'ouest
            status = hr.turn_clockwise()
            know.ajout_voir_knowledge(status)
    elif pos == (0,m-1):
        # on doit regarder a l'est et au sud
        if orientation == HC.S:
            #on regarde a l'est
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
        elif orientation == HC.E:
            #on regarde au sud
            status = hr.turn_clockwise()
            know.ajout_voir_knowledge(status)
        elif orientation == HC.N:
            #on regarde a l'est
            status = hr.turn_clockwise()
            know.ajout_voir_knowledge(status)
            #on regarde au sud
            status = hr.turn_clockwise()
            know.ajout_voir_knowledge(status)
        elif orientation == HC.W:
            #on regarde au sud
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)

    elif pos in bordure_N:
        # on doit regarder a l'ouest, a l'est et au sud
        if orientation == HC.N:
            #on regarde a l'ouest
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
            #on regarde a sud
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
            # on regarde a l'est
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
        elif orientation == HC.E:
            #on regarde au sud
            status = hr.turn_clockwise()
            know.ajout_voir_knowledge(status)
            #on regarde a l'ouest
            status = hr.turn_clockwise()
            know.ajout_voir_knowledge(status)
        elif orientation == HC.S:
            #on regarde a l'ouest
            status = hr.turn_clockwise()
            know.ajout_voir_knowledge(status)
            #on regarde a l'est
            status = hr.turn_clockwise()
            know.ajout_voir_knowledge(status)
            status = hr.turn_clockwise()
            know.ajout_voir_knowledge(status)
        elif orientation == HC.W:
            #on regarde au sud
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
            #on regarde a l'est
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
    elif pos in bordure_S:
        # on doit regarder a l'ouest, a l'est et au nord
        if orientation == HC.S:
            #on regarde a l'ouest
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
            #on regarde a nord
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
            # on regarde a l'est
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
        elif orientation == HC.E:
            #on regarde au nord
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
            #on regarde a l'ouest
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
        elif orientation == HC.N:
            #on regarde a l'ouest
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
            #on regarde a l'est
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
        elif orientation == HC.W:
            #on regarde au nord
            status = hr.turn_clockwise()
            know.ajout_voir_knowledge(status)
            #on regarde a l'est
            status = hr.turn_clockwise()
            know.ajout_voir_knowledge(status)
    elif pos in bordure_E:
        # on doit regarder au nord, a l'ouest et au sud
        if orientation == HC.E:
            #on regarde au nord
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
            #on regarde a l'ouest
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
            # on regarde au sud
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
        elif orientation == HC.S:
            #on regarde a l'ouest
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
            #on regarde au nord
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
        elif orientation == HC.W:
            #on regarde au nord
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
            #on regarde au sud
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
        elif orientation == HC.N:
            #on regarde a l'ouest
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
            #on regarde au sud
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
    elif pos in bordure_W:
        # on doit regarder au nord, a l'est et au sud
        if orientation == HC.W:
            #on regarde au nord
            status = hr.turn_clockwise()
            know.ajout_voir_knowledge(status)
            #on regarde a l'est
            status = hr.turn_clockwise()
            know.ajout_voir_knowledge(status)
            # on regarde au sud
            status = hr.turn_clockwise()
            know.ajout_voir_knowledge(status)
        elif orientation == HC.S:
            #on regarde a l'est
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
            #on regarde au nord
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
        elif orientation == HC.E:
            #on regarde au nord
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
            #on regarde au sud
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
            status = hr.turn_anti_clockwise()
            know.ajout_voir_knowledge(status)
        elif orientation == HC.N:
            #on regarde a l'est
            status = hr.turn_clockwise()
            know.ajout_voir_knowledge(status)
            #on regarde au sud
            status = hr.turn_clockwise()
            know.ajout_voir_knowledge(status)
    return status