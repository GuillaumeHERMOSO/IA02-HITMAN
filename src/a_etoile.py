from typing import Callable, Dict, List, Optional, Tuple
State = tuple[int, int]
from src.arbitre.hitman import *
from src.Class_HitmanKnowledge import *

def distanceManhattan(s1: State , s2: State):
    return abs(s1[0] - s2[0]) + abs(s1[1] - s2[1])

def nbr_wall_entre(s1: State, s2: State, walls: List[State]):
    """Retourne le nombre de murs entre s1 et s2 pour cela
    on regarde si les deux états sont sur la même ligne ou la même colonne
    si c'est le cas on regarde si il y a un mur entre les deux états
    """
    nbr = 0
    if s1[0] == s2[0]:
        for i in range(min(s1[1], s2[1]), max(s1[1], s2[1])):
            if (s1[0], i) in walls:
                nbr += 1
    elif s1[1] == s2[1]:
        for i in range(min(s1[0], s2[0]), max(s1[0], s2[0])):
            if (i, s1[1]) in walls:
                nbr += 1
    else:
        # On a est pas sur la même ligne ou la même colonne donc on compte les murs entre les deux états en partant par le haut puis par la droite
        nbr += nbr_wall_entre(s1, (s1[0], s2[1]), walls)
        nbr += nbr_wall_entre((s1[0], s2[1]), s2, walls)

    return nbr

def is_case_vu(s: State, case_vu: List[State]) -> bool:
    if s in case_vu:
        return True
    return False

def heuristique1(s0 : State, s: State, goal: State, walls: List[State], case_vu: List[State], map : dict[tuple[int, int], HC], visited ) -> int:
    """Heuristique qui consiste à calculer la distance de Manhattan entre l'état courant et l'état goal
    et à ajouter le nombre de murs entre les deux états
    """
    if map[s] == HC.WALL:
        return
    #10* nbr_wall_entre(s, goal, walls)
    a = 0
    if s in visited:
        a = 5
    return distanceManhattan(s, s0) + distanceManhattan(s, goal) + 5*is_case_vu(s, case_vu) + a

def insert_avec_heuristique(s0 :State,s : State, l : List[State], goal : State, walls : List[State], case_vu: List[State], map, visited) -> List[State]:
    """Insertion dans la liste l de l'état s en fonction de l'heuristique"""
    l.append(s)
    if len(l) > 1:
        l.sort(key=lambda x: heuristique1(s0,x, goal, walls, case_vu, map, visited))
    return l

def remove_1(l):
    # On enleve le premier element de la liste
    return l.pop(0), l

def succ(s: State, m: int, n:int, dico_val: dict[tuple[int, int], HC] ) -> List[State]:
    """Retourne les successeurs de l'état s on verifira les bordures de la carte"""
    # On ajoute dans l'ordre droite, bas, gauche, haut
    l = []
    if s[0] < n-1 and (s[0]+1, s[1]) in dico_val.keys() and dico_val[(s[0]+1, s[1])] in [HC.EMPTY, HC.SUIT, HC.TARGET, HC.CIVIL_E, HC.CIVIL_S, HC.CIVIL_W, HC.CIVIL_N]:
        l.append((s[0]+1, s[1]))

    if s[0] >0 and (s[0]-1, s[1]) in dico_val.keys() and dico_val[(s[0]-1, s[1])] in [HC.EMPTY, HC.SUIT, HC.TARGET, HC.CIVIL_E, HC.CIVIL_S, HC.CIVIL_W, HC.CIVIL_N]:
        l.append((s[0]-1, s[1]))

    if s[1] > 0 and (s[0], s[1]-1) in dico_val.keys() and dico_val[(s[0], s[1]-1)] in [HC.EMPTY, HC.SUIT, HC.TARGET, HC.CIVIL_E, HC.CIVIL_S, HC.CIVIL_W, HC.CIVIL_N]:
        l.append((s[0], s[1]-1))

    if s[1] < m-1 and (s[0], s[1]+1) in dico_val.keys() and dico_val[(s[0], s[1]+1)] in [HC.EMPTY, HC.SUIT, HC.TARGET, HC.CIVIL_E, HC.CIVIL_S, HC.CIVIL_W, HC.CIVIL_N]:
        l.append((s[0], s[1]+1))
    return l



def gen_test_map(a,b) ->dict[tuple[int, int], str]:
    """ Generation de carte aleatoire pour tester l'heuristique """
    import random
    walls = []
    case_vu = []
    dict_map = {}
    for i in range(a):
        for j in range(b):
            # on ajoute un mur 0.1 ou on est vu par un garde 0.2 ou rien
            if random.random() < 0.1:
                walls.append((i,j))
                dict_map[(i,j)] = "mur"
            elif random.random() < 0.2:
                case_vu.append((i,j))
                dict_map[(i,j)] = "vu "
            else:
                dict_map[(i,j)] = "   "
    dict_map[(0,0)] = "   "
    dict_map[(0,1)] = "   "
    dict_map[(1,0)] = "   "
    dict_map[(8,9)] = "   "
    dict_map[(9,8)] = "   "
    dict_map[(9,9)] = "   "
    return dict_map, walls, case_vu

def print_map(dict_map: dict[tuple[int, int], str], walls: List[State], case_vu: List[State]):
    """ Affichage de la carte """
    for i in range(10):
        for j in range(10):
            if (i,j) in walls:
                print("X", end=" | ")
            elif (i,j) in case_vu:
                print("O", end=" | ")
            else:
                print(" ", end=" | ")
        print()

def astar_with_parent(
                    s0: State,
                    goals: List[State],
                    succ: Callable[[State], List[State]],
                    dico_val: dict[tuple[int, int], HC], 
                    m: int,
                    n: int,
                    walls: List[State], 
                    case_vu: List[State],
                    visited: List [State]) -> Tuple[Optional[State], Dict[State, Optional[State]]]:
    """A* avec parent"""
    d = {}
    d[s0] = None
    l = [s0]
    while l != []:
        s, l = remove_1(l)
        if s in goals:
            return s, d
        for s2 in succ(s, m, n, dico_val):
            if s2 not in d:
                d[s2] = s
                l = insert_avec_heuristique(s0, s2, l, goals[0], walls, case_vu, dico_val, visited)
        print(f"l : {l}")
    return None, d

def coup_chemin (l : List[State], map : dict[tuple[int, int], str], ) -> int:
    """Retourne le nombre de coup pour parcourir le chemin 1 si on avance + 5 si on est vu"""
    cpt = 0
    for i in range(len(l)-1):     
        if map[l[i]] == "vu ":
            cpt += 5
        else:
            cpt += 1
    return cpt

def case_connu_qui_peut_voir_une_case(case : State, m:int, n:int, dico_val : dict[tuple[int, int], HC]) -> Tuple[List[State], dict[State, HC]]:
    """ fct qui retourne les postion qui peuvent voir la case sachant qu'on peut voir a 3 cases de distance si il y a rien devant"""
    case_pour_voir = []
    orientation_a_obtenir = {}
    # soit c'est vide
    for a in range(1,4):
        if case[0]+a < n and (case[0]+a,case[1]) in dico_val.keys() and dico_val[(case[0]+a,case[1])] in [HC.SUIT, HC.TARGET, HC.CIVIL_E, HC.CIVIL_S, HC.CIVIL_W, HC.CIVIL_N]:
            case_pour_voir.append((case[0]+a,case[1]))
            break
        if case[0]+a < n and (case[0]+a,case[1]) in dico_val.keys() and dico_val[(case[0]+a,case[1])] == HC.EMPTY:
            case_pour_voir.append((case[0]+a,case[1]))
        else:
            break
    for a in range(1,4):
        if case[0]-a >= 0 and (case[0]-a,case[1]) in dico_val.keys() and dico_val[(case[0]-a,case[1])] in [HC.SUIT, HC.TARGET, HC.CIVIL_E, HC.CIVIL_S, HC.CIVIL_W, HC.CIVIL_N]:
            case_pour_voir.append((case[0]-a,case[1]))
            break
        if case[0]-a >= 0 and (case[0]-a,case[1]) in dico_val.keys() and dico_val[(case[0]-a,case[1])] == HC.EMPTY:
            case_pour_voir.append((case[0]-a,case[1]))
        else:
            break
    for a in range(1,4):
        if case[1]+a < m and (case[0],case[1]+a) in dico_val.keys() and dico_val[(case[0],case[1]+a)] in [HC.SUIT, HC.TARGET, HC.CIVIL_E, HC.CIVIL_S, HC.CIVIL_W, HC.CIVIL_N]:
            case_pour_voir.append((case[0],case[1]+a))
            break
        if case[1]+a < m and (case[0],case[1]+a) in dico_val.keys() and dico_val[(case[0],case[1]+a)] == HC.EMPTY:
            case_pour_voir.append((case[0],case[1]+a))
        else:
            break
    for a in range(1,4):
        if case[1]-a >= 0 and (case[0],case[1]-a) in dico_val.keys() and dico_val[(case[0],case[1]-a)] in [HC.SUIT, HC.TARGET, HC.CIVIL_E, HC.CIVIL_S, HC.CIVIL_W, HC.CIVIL_N]:
            case_pour_voir.append((case[0],case[1]-a))
            break
        if case[1]-a >= 0 and (case[0],case[1]-a) in dico_val.keys() and dico_val[(case[0],case[1]-a)] == HC.EMPTY:
            case_pour_voir.append((case[0],case[1]-a))
        else:
            break
    for c in case_pour_voir:
        if c[0] == case[0]:
            if c[1] > case[1]:
                orientation_a_obtenir[c] = HC.S
            else:
                orientation_a_obtenir[c] = HC.N
        else:
            if c[0] > case[0]:
                orientation_a_obtenir[c] = HC.W
            else:
                orientation_a_obtenir[c] = HC.E
    return case_pour_voir, orientation_a_obtenir

def main1():
    map, walls, case_vu = gen_test_map(10,10)
    print(walls, case_vu)
    print_map(map, walls, case_vu)
    print("Début de l'algo")
    s0 = (0,0)
    goal = (9,9)
    s, d = astar_with_parent(s0, goal, succ, map, walls, case_vu)
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
    print("Nombre de coup pour parcourir le chemin : ", coup_chemin(chemin, map))

def main():
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
    con = HitmanKnowledge(m=6, n=6)
    con.knowledge = complete_map_example
    print(con)
if __name__ == "__main__":
    main()