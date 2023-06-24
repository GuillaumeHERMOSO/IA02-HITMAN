from enum import Enum
from time import sleep
from typing import Tuple, Dict, List
Grid = List[List[int]]
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]
Model = List[Literal]

from src.arbitre.hitman import *

class HitmanKnowledge:
    def __init__(self, m: int, n: int):
        self.m = m
        self.n = n
        self.knowledge = {}
        self.matrice_vision = {}
        self.matrice_vision_civil = {}
    
    def has_knowledge(self, i: int, j: int) -> bool:
        return (i, j) in self.knowledge


    def orientation_garde(self,garde : HC):
        if garde in [HC.GUARD_N, HC.N, HC.CIVIL_N]:
            offset = 0, 1
        elif garde in [HC.GUARD_E, HC.E, HC.CIVIL_E]:
            offset = 1, 0
        elif garde in [HC.GUARD_S, HC.S, HC.CIVIL_S]:
            offset = 0, -1
        elif garde in [HC.GUARD_W, HC.W , HC.CIVIL_W]:
            offset = -1, 0
        return offset
    
    def quadri_direction(self,position): 
    # Ajoute dans la matrice de vision les 4 directions pour une personne deduite non vu ( HC.N )
        direction = [HC.N,HC.E,HC.S,HC.W]
        vision = []
        for direc in direction :
            offset_x, offset_y = self.orientation_garde(direc)
            x, y = position
            for _ in range(0, 2):
                pos = x + offset_x, y + offset_y
                x, y = pos
                if x >= self.n or y >= self.m or x < 0 or y < 0:
                    break
                vision.append(pos)
                if (self.has_knowledge(x, y) and self.knowledge[pos] != HC.EMPTY):
                    break
        return vision
    def maj_vision_garde (self) :

        self.matrice_vision = {(i,j):0 for i in range(self.n) for j in range(self.m)}
        for position in self.knowledge:
            vision = []
            if self.knowledge[position] in  [HC.GUARD_N,HC.GUARD_E,HC.GUARD_S,HC.GUARD_W]:
                offset_x, offset_y = self.orientation_garde(self.knowledge[position])
                x,y = position
                for _ in range(0, 2):
                    pos = x + offset_x, y + offset_y
                    x, y = pos
                    if x >= self.n or y >= self.m or x < 0 or y < 0:
                        break
                    vision.append(pos)
                    if (self.has_knowledge(x,y) and self.knowledge[pos] != HC.EMPTY):
                        break
            elif self.knowledge[position] == HC.N :
                vision_quadri = self.quadri_direction(position)
                if len(vision_quadri) > 0 :
                    for elt in vision_quadri :
                        vision.append(elt)
            for pos in vision:
                self.matrice_vision[pos] += 1

        pass

    def maj_vision_civil (self) :
        
        self.matrice_vision_civil = {(i,j):0 for i in range(self.n) for j in range(self.m)}
        for position in self.knowledge:
            vision = []
            if self.knowledge[position] in  [HC.CIVIL_N,HC.CIVIL_E,HC.CIVIL_S,HC.CIVIL_W]:
                offset_x, offset_y = self.orientation_garde(self.knowledge[position])
                x,y = position
                for _ in range(0, 2):
                    pos = x + offset_x, y + offset_y
                    x, y = pos
                    if x >= self.n or y >= self.m or x < 0 or y < 0:
                        break
                    vision.append(pos)
                    if (self.has_knowledge(x,y) and self.knowledge[pos] != HC.EMPTY):
                        break
            for pos in vision:
                self.matrice_vision_civil[pos] += 1

        pass
        

    def add_knowledge(self, position: Tuple[int, int], content: HC):
        if (not self.has_knowledge(position[0], position[1]) or self.knowledge[position] in [HC.N]):
            self.knowledge[position] = content
            self.maj_vision_garde()
            pass
        pass

    def get_knowledge(self, position: Tuple[int, int]) -> HC:
        if self.has_knowledge(position[0], position[1]):
            return self.knowledge[position]
        return None

    def get_all_knowledge(self) -> Dict[Tuple[int, int], HC]:
        return self.knowledge
 
    def get_no_knowledge_clause(self,dict_var_to_num)-> List[int] :
        variables_a_tester = []
        for j in range(self.m):
            for i in range(self.n):
                if not self.has_knowledge(i, j):              # Si on a pas de connaissances, c'est une variable à tester
                    variables_a_tester.append(dict_var_to_num[f"{i}{j}_P"])
        return variables_a_tester

                

    def __str__(self) -> str:
        """Affichage de la matrice de connaissance avec 0,0 en bas à gauche, en haut a gauche (0,m) et (n,m) en haut à droite, si il y a rien on affiche x"""
        r =""
        for j in range(self.m-1,-1,-1):
            r += str(j) + "      "
            for i in range(self.n):
                if self.has_knowledge(i,j):
                    #format permet d'avoir la meme taille pour chaque case  max 10 caractere, ^ pour centrer
                    r += format(self.get_knowledge((i,j)).name,"^11") +" "

                else:
                    r += format("x","^11") +" "
            r +="\n"
        # affichage des indices en bas 0,1, ... , n-1
        r += "       " + " ".join([format(str(i),"^11") for i in range(self.n)])
        return r

    
    def affichage_vison(self):
        r =""
        for j in range(self.m-1,-1,-1):
            r += str(j) + "      "
            for i in range(self.n):
                r += format(self.matrice_vision[(i,j)],"^11") +" "
            r +="\n"
        # affichage des indices en bas 0,1, ... , n-1
        r += "       " + " ".join([format(str(i),"^11") for i in range(self.n)])
        print (r)
        pass

    def ajout_voir_knowledge(self, status: Dict):
        for pos,valeur in status["vision"] :
            self.add_knowledge(pos,valeur)
        pass

    def je_sais_pas_tt(self):
        #boolean pour savoir si notre dico est complet
        for i in range(self.n):
            for j in range(self.m):
                if not self.has_knowledge(i,j):
                    return True
                if self.knowledge[(i,j)] in [HC.N]:
                    return True
        return False

    def get_liste_mur(self)->List[Tuple[int,int]]:
        """Retourne la liste des murs"""
        r = []
        for pos,val in self.knowledge.items():
            if val == HC.WALL:
                r.append(pos)
        return r
    
    def get_liste_casevu(self)->List[Tuple[int,int]]:
        """Retourne la liste des cases vues"""
        self.maj_vision_garde()
        r = []
        for pos,val in self.matrice_vision.items():
            if val != 0:
                r.append(pos)
        return r

    def get_liste_casevu_civil(self)->List[Tuple[int,int]]:
        """Retourne la liste des cases vues"""
        self.maj_vision_civil()
        r = []
        for pos,val in self.matrice_vision.items():
            if val != 0:
                r.append(pos)
        return r

    
def knowledge_to_clause_personne(Dico_know : Dict[Tuple[int, int], HC], dict_var_to_num : Dict[str, int])-> ClauseBase:
    r : ClauseBase = [] 
    for i,v in Dico_know.items():
        #print(v)
        if v in [HC.CIVIL_E, HC.CIVIL_N, HC.CIVIL_S, HC.CIVIL_W, HC.GUARD_E, HC.GUARD_N, HC.GUARD_S, HC.GUARD_W, HC.N]:
            r.append(dict_var_to_num[f"{i[0]}{i[1]}_P"]) 
    return r



def transpose_tableau(tableau):
    n = len(tableau)
    m = len(tableau[0])
    tableau_transpose_inverse = [[0] * n for _ in range(m)]

    for i in range(n):
        for j in range(m):
            tableau_transpose_inverse[j][i] = tableau[i][j]

    tableau_transpose_inverse.reverse()



    return tableau_transpose_inverse

def ajouter_zeros_autour(tableau_original):
    n = len(tableau_original)
    i = 0
    m = len(tableau_original[i])
    tableau_resultat = [[0] * (3 * m) for _ in range(3 * n)]

    for i in range(n):
        for j in range(m):
            x = 3 * i + 1
            y = 3 * j + 1
            tableau_resultat[x][y] = tableau_original[i][j]

    return tableau_resultat

def afficher(hc : HitmanKnowledge, hr: HitmanReferee, dico : dict) :
    tableau = []
    x,y = dico["position"] # Position de Hitman
    for i in range(hc.n) :
        tableau.append([])
        for j in range(hc.m) :
            if (i, j) == (x, y):  # rajout d'Hitman ( vue de haut )
                tableau[i].append("O")
            elif hc.has_knowledge(i, j) : # Si on a des connaissances
                tableau[i].append(hc.get_knowledge((i, j)))
            else :
                tableau[i].append("X")
        #print(tableau[i])
    tableau_resultat = ajouter_zeros_autour(transpose_tableau(tableau)) # tableau bien mis ( (0,m) = en haut a gauche , (n,m) = en haut a droite )
    tab_finale = []
    x_1 = 0
    y_1 = 0

    for i in range(len(tableau_resultat)):
        tab_finale.append([])
        for j in range(len(tableau_resultat[i])):
            if tableau_resultat[i][j] == "O" :
                tab_finale[i].append("O")
                x_1 = i
                y_1 = j
            elif tableau_resultat[i][j] == "X" :
                tab_finale[i].append("X")
            else :
                tab_finale[i].append(" ")

    if dico["orientation"] == HC.S:
        tab_finale[x_1+1][y_1] = "v"
    elif dico["orientation"] == HC.N:
        tab_finale[x_1-1][y_1] = "^"
    elif dico["orientation"] == HC.E:
        tab_finale[x_1][y_1+1] = ">"
    elif dico["orientation"] == HC.W:
        tab_finale[x_1][y_1-1] = "<"


    for li in range(len(tableau_resultat)) :
        for col in range(len(tableau_resultat[li])) :
            if tableau_resultat[li][col] in [HC.GUARD_N,HC.GUARD_E,HC.GUARD_S,HC.GUARD_W] :
                nv_val = "G"
                if tableau_resultat[li][col] == HC.GUARD_S: # Sud
                    tab_finale[li][col] = "G"
                    tab_finale[li+1][col] = "v"
                elif tableau_resultat[li][col] == HC.GUARD_N:
                    tab_finale[li][col] = nv_val
                    tab_finale[li-1][col] = "^"
                elif tableau_resultat[li][col] == HC.GUARD_E: # est
                    tab_finale[li][col] = nv_val
                    tab_finale[li][col+1] = ">"
                elif tableau_resultat[li][col] == HC.GUARD_W : # Ouest
                    tab_finale[li][col] = nv_val
                    tab_finale[li][col-1] = "<"
            elif tableau_resultat[li][col] in [HC.CIVIL_N,HC.CIVIL_E,HC.CIVIL_S,HC.CIVIL_W] :
                nv_val = "C"
                if tableau_resultat[li][col] == HC.CIVIL_S:
                    tab_finale[li][col] = nv_val
                    tab_finale[li + 1][col] = "v"
                elif tableau_resultat[li][col] == HC.CIVIL_N:
                    tab_finale[li][col] = nv_val
                    tab_finale[li - 1][col] = "^"
                elif tableau_resultat[li][col] == HC.CIVIL_E:
                    tab_finale[li][col] = nv_val
                    tab_finale[li][col + 1] = ">"
                elif tableau_resultat[li][col] == HC.CIVIL_W:
                    tab_finale[li][col] = nv_val
                    tab_finale[li][col - 1] = "<"
            elif tableau_resultat[li][col] == HC.WALL : # Construction d'un mur visuel

                if col+2 < len(tableau_resultat[li]) :
                    if tab_finale[li][col+2] != '┃' :  ## Est
                        tab_finale[li][col+1] = '┃'
                        tab_finale[li + 1][col + 1] = '┃'
                        tab_finale[li - 1][col + 1] = '┃'
                    elif tab_finale[li][col+2] == '┃' :
                        tab_finale[li - 1][col + 2] = '━'
                        tab_finale[li][col + 2] = " "
                        tab_finale[li + 1][col + 2] = '━'
                        if li+2<len(tableau_resultat) :
                            if tab_finale[li+2][col+2] == '┃':
                                tab_finale[li + 1 ][col + 2] = "┓"
                        if li - 2 >= 0:
                            if tab_finale[li - 2][col+2] == '┃' :
                                tab_finale[li - 1][col + 2] = "┛"


                if col-2 >=0 :
                    if tab_finale[li][col-2] != '┃' :  ## Ouest
                        tab_finale[li - 1][col - 1] = '┃'
                        tab_finale[li][col-1] = '┃'
                        tab_finale[li + 1][col - 1] = '┃'
                    elif tab_finale[li][col-2] == '┃' :
                        tab_finale[li - 1][col - 2] = '━'
                        tab_finale[li][col - 2] = " "
                        tab_finale[li + 1][col - 2] = '━'
                        if li+2<len(tableau_resultat) :
                            if tab_finale[li+2][col-2] == '┃':
                                tab_finale[li + 1 ][col - 2] = '┏'
                        if li - 2 >= 0:
                            if tab_finale[li - 2][col-2] == '┃' :
                                tab_finale[li - 1][col - 2] = "┗"


                if li-2 >=0 :
                    if tab_finale[li-2][col] != '━' :  ## Nord
                        tab_finale[li - 1][col-1] = '━'
                        tab_finale[li - 1][col] = '━'
                        tab_finale[li - 1][col+1] = '━'
                    elif tab_finale[li-2][col] == '━' :
                        tab_finale[li - 2][col - 1] = '┃'
                        tab_finale[li - 2][col] = " "
                        tab_finale[li - 2][col + 1] = '┃'
                        if col - 2 >= 0:
                            if tab_finale[li - 2][col - 2] == '━':
                                tab_finale[li - 2][col - 1] = "┓"
                        if col + 2 < len(tableau_resultat[li]):
                            if tab_finale[li - 2][col + 2] == '━':
                                tab_finale[li - 2][col + 1] = '┏'

                if li+2<len(tableau_resultat) :
                    if tab_finale[li + 2][col] != '━' :  ## Sud
                        tab_finale[li + 1][col - 1] = '━'
                        tab_finale[li + 1][col] = '━'
                        tab_finale[li + 1][col + 1] = '━'
                    elif tab_finale[li + 2][col] == '━' :
                        tab_finale[li + 2][col - 1] = '┃'
                        tab_finale[li + 2][col] = " "
                        tab_finale[li + 2][col + 1] = '┃'
                        if col - 2 >= 0:
                            if tab_finale[li + 2][col - 2] == '━':
                                tab_finale[li + 2][col - 1] = "┛"
                        if col + 2 <len(tableau_resultat[li]):
                            if tab_finale[li + 2][col + 2] == '━':
                                tab_finale[li + 2][col + 1] = "┗"

            elif tableau_resultat[li][col] == HC.SUIT :
                tab_finale[li][col] = "S"
            elif tableau_resultat[li][col] == HC.TARGET:
                tab_finale[li][col] = "T"
            elif tableau_resultat[li][col] == HC.PIANO_WIRE:
                tab_finale[li][col] = "P"
            elif tableau_resultat[li][col] == HC.EMPTY:
                tab_finale[li][col] = " "




    # Affichage du tableau finale
    for ligne in tab_finale:

        for elt in ligne:
            print(elt, end="  ")
        print()





