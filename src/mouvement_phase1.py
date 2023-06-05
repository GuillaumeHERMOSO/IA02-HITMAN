from src.arbitre.hitman import *
from src.Class_HitmanKnowledge import *

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

def case_inconnu_plus_proche_hitman(x :int, y :int,n: int, m:int, know :HitmanKnowledge):
    dist = 99999999
    #(i,j) x sur m et y sur n
    for i in range(n):
        for j in range(m):
            if (i,j) not in know.knowledge:
                if abs(i-x) + abs(j-y) < dist:
                    dist = abs(i-x) + abs(j-y)
                    case = (i,j)
    return case
def case_ok (x:int ,y: int ,n: int, m:int, know :HitmanKnowledge):
    if x >= 0 and x<=m and y >= 0 and y<=n :
        if (x,y) not in know.knowledge:
            return True
        elif know.knowledge[(x,y)] not in [HC.GUARD_E,HC.GUARD_N,HC.GUARD_S,HC.GUARD_W, HC.WALL]:
            return True
    return False

def case_possible (x:int ,y: int ,n: int, m:int, know :HitmanKnowledge):
    if x >= 0 and x<=m and y >= 0 and y<=n :
        if (x,y) not in know.knowledge:
            return True
        elif know.knowledge[(x,y)] != HC.WALL:
            return True
    return False

def liste_case_ok(x:int ,y: int ,n: int, m:int, know :HitmanKnowledge):
    liste = []
    if case_ok(x+1,y,n,m,know):
        liste.append((x+1,y))
    if case_ok(x-1,y,n,m,know):
        liste.append((x-1,y))
    if case_ok(x,y+1,n,m,know):
        liste.append((x,y+1))
    if case_ok(x,y-1,n,m,know):
        liste.append((x,y-1))
    return liste


def successeur_case(x:int , y:int ,val:HC, n:int, m:int, know :HitmanKnowledge):
    if val in [HC.GUARD_E,HC.GUARD_N,HC.GUARD_S,HC.GUARD_W, HC.WALL] :
        return None
    else :
        return liste_case_ok(x,y,n,m,know)
    


def strategie1(hr :HitmanReferee, Knowledge : HitmanKnowledge) :
    """ Strategie 1 : on est sur une case on tourne pour voir tt les cases autour de nous si on en a pas la connaissance 
    puis on avance d'une case en priorisant les case qui sont le moins vu par les gardes et sinon on prend lautre Nord ouest sud est
    """
    status = hr.start_phase1()
    n = status["n"]
    m = status["m"]
    x,y = status["position"]
    orientation = status["orientation"]
    
   
    #strategie : on va vers le nord si on a pas la connaissance de la case nord +3
    orientation = status["orientation"]
    if orientation == HC.N:
        dest = (x,y+3)
        verif = (x,y+1)
    elif orientation == HC.E:
        dest = (x+3,y)
        verif = (x+1,y)
    elif orientation == HC.S:
        dest = (x,y-3)
        verif = (x,y-1)
    elif orientation == HC.W:
        dest = (x-3,y)
        verif = (x-1,y)
    
    if Knowledge.has_knowledge(dest[0],dest[1]) == False:
        #on va vers notre orientation car on a pas la connaissance de la case +3
        if case_ok(dest[0], dest[1], n, m, Knowledge):
            print(f"on va vers la case {dest} car on a pas la connaissance de la case +3")
            if case_possible(verif[0], verif[1], n, m, Knowledge):
                print(f"on avance pour avoir la connaissance de la case +3")
                status = hr.move()
                Knowledge.ajout_voir_knowledge(status)
                return status
            else:
                print(f"on tourne car on peut pas allez en +1")
                status = hr.turn_clockwise()
                Knowledge.ajout_voir_knowledge(status)
                return status
        else:
            print(f"on tourne car on a  la connaissance de la case +3")
            status = hr.turn_clockwise()
            Knowledge.ajout_voir_knowledge(status)
            return status
    else:
        print("on tourne car on a pas la connaissance de la case +3")
        status = hr.turn_clockwise()
        Knowledge.ajout_voir_knowledge(status)
        if orientation == HC.N:
            dest = (x,y+3)
        elif orientation == HC.E:
            dest = (x+3,y)
        elif orientation == HC.S:
            dest = (x,y-3)
        elif orientation == HC.W:
            dest = (x-3,y)
        
        if case_possible(dest[0], dest[1], n, m, Knowledge):
            print(f"on va vers la case {dest} car on a pas la connaissance de la case +3")
            status = hr.move()
            Knowledge.ajout_voir_knowledge(status)
            return status
        return status





"""
    if x<n and dico_connaissance[(x + 1, y)] == "Vide" : # Si le nord est inconnu
        if orientation == (1, 0):  # Si à l'est
            dico = HitmanReferee.turn_clockwise()
            dico_connaissance = maj_dico_connaissance(dico_connaissance,dico)
            maj_fichier_sat_vision(dico)
        else:  # Si Ouest ou Sud(opposé de nord )
            dico = HitmanReferee.turn_anti_clockwise()
            dico_connaissance = maj_dico_connaissance(dico_connaissance,dico)
            maj_fichier_sat_vision(dico)

    if x>0 and dico_connaissance[(x - 1, y)] == "Vide": # Si le sud est inconnu
        if orientation == (-1, 0):  # Si à l'ouest
            dico = HitmanReferee.turn_clockwise()
            dico_connaissance = maj_dico_connaissance(dico_connaissance,dico)
            maj_fichier_sat_vision(dico)
        else:  # Si Est ou nord(opposé de sud )
            dico = HitmanReferee.turn_anti_clockwise()
            dico_connaissance = maj_dico_connaissance(dico_connaissance,dico)
            maj_fichier_sat_vision(dico)


    if y<m and dico_connaissance[(x, y+1)] == "Vide": # Si l'est est inconnu
        if orientation == (0, 1):  # Si au Nord
            dico = HitmanReferee.turn_clockwise()
            dico_connaissance = maj_dico_connaissance(dico_connaissance,dico)
            maj_fichier_sat_vision(dico)

        else:  # Si Sud ou Ouest(opposé de l'est )
            dico = HitmanReferee.turn_anti_clockwise()
            dico_connaissance = maj_dico_connaissance(dico_connaissance,dico)
            maj_fichier_sat_vision(dico)


    if y>0 and dico_connaissance[(x, y - 1)] == "Vide": # Si l'ouest est inconnu
        if orientation == (0, -1):  # Si au Sud
            dico = HitmanReferee.turn_clockwise()
            dico_connaissance = maj_dico_connaissance(dico_connaissance,dico)
            maj_fichier_sat_vision(dico)

        else:  # Si Nord ou Est (opposé de l'ouest )
            dico = HitmanReferee.turn_anti_clockwise()
            dico_connaissance = maj_dico_connaissance(dico_connaissance,dico)
            maj_fichier_sat_vision(dico)

    # Normalement d'ici on a toutes les données des 4 orientations

    if orientation == (0,1) and x<n and matrice_vision[x+1][y] == 0 and dico_connaissance[(x+1,y)] not in [HC.WALL,HC.GUARD_W,HC.GUARD_N,HC.GUARD_E,HC.GUARD_S] :
        return HitmanReferee.move()
    if orientation == (0,-1) and x>0 and matrice_vision[x-1][y] == 0 and dico_connaissance[(x-1,y)] not in [HC.WALL,HC.GUARD_W,HC.GUARD_N,HC.GUARD_E,HC.GUARD_S] :
        return HitmanReferee.move()
    if orientation == (1,0) and y<m and matrice_vision[x][y+1] == 0 and dico_connaissance[(x,y+1)] not in [HC.WALL,HC.GUARD_W,HC.GUARD_N,HC.GUARD_E,HC.GUARD_S] :
        return HitmanReferee.move()
    if orientation == (-1,0) and y>0 and matrice_vision[x][y-1] == 0 and dico_connaissance[(x,y-1)] not in [HC.WALL,HC.GUARD_W,HC.GUARD_N,HC.GUARD_E,HC.GUARD_S] :
        return HitmanReferee.move()

    return dico
    """