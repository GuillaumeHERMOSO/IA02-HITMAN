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
    
    def has_knowledge(self, i: int, j: int) -> bool:
        return (i, j) in self.knowledge
    
    def orientation_garde(self,garde):
        if garde in [HC.GUARD_N, HC.N]:
            offset = 0, 1
        elif garde in [HC.GUARD_E, HC.E]:
            offset = 1, 0
        elif garde in [HC.GUARD_S, HC.S]:
            offset = 0, -1
        elif garde in [HC.GUARD_W, HC.W]:
            offset = -1, 0
        return offset
    
    def maj_vision_garde (self) :
        """ Mettre a jour la matrice de vision des gardes """
        #TODO voir si on peut faire autrement pour ne pas tt init

        self.matrice_vision = {(i,j):0 for i in range(self.n) for j in range(self.m)}
        for position in self.knowledge:
            vision = []
            if self.knowledge[position] in  [HC.GUARD_N,HC.GUARD_E,HC.GUARD_S,HC.GUARD_W, HC.N, HC.E, HC.S, HC.W]:
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
                self.matrice_vision[pos] += 1
        pass

    def add_knowledge(self, position: Tuple[int, int], content: HC):
        if (not self.has_knowledge(position[0], position[1]) or self.knowledge[position] in [HC.N, HC.E, HC.S, HC.W]):
            self.knowledge[position] = content
            self.maj_vision_garde()
            pass
        #print("Erreur : la position est déjà connue")
        pass

    def get_knowledge(self, position: Tuple[int, int]) -> HC:
        if self.has_knowledge(position[0], position[1]):
            return self.knowledge[position]
        return None

    def get_all_knowledge(self) -> Dict[Tuple[int, int], HC]:
        return self.knowledge
 

                

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
        if status["is_in_guard_range"]:
            # on est vu en position pos 
            print(f"\n\n\non est vu en position {status['position']} on mets des gardes potentiel")
            pos = status["position"]
            # on verifie si on a pas deja l'info :
            a_nord = [(pos[0],pos[1]+1),(pos[0],pos[1]+2)]
            for pos in a_nord :
                if self.has_knowledge(pos[0],pos[1]) and self.knowledge[pos] == HC.GUARD_S:
                    return
            a_sud = [(pos[0],pos[1]-1),(pos[0],pos[1]-2)]
            for pos in a_sud :
                if self.has_knowledge(pos[0],pos[1]) and self.knowledge[pos] == HC.GUARD_N:
                    return
            a_est = [(pos[0]+1,pos[1]),(pos[0]+2,pos[1])]
            for pos in a_est :
                if self.has_knowledge(pos[0],pos[1]) and self.knowledge[pos] == HC.GUARD_W:
                    return
            if (pos[1]+1 < self.m):
                self.add_knowledge((pos[0],pos[1]+1),HC.S)
            if (pos[1]+2 < self.m):
                self.add_knowledge((pos[0],pos[1]+2),HC.S)
            if (pos[0]+1 < self.n):
                self.add_knowledge((pos[0]+1,pos[1]),HC.W)
            if (pos[0]+2 < self.n):
                self.add_knowledge((pos[0]+2,pos[1]),HC.W)
            if (pos[1]-1 >= 0):
                self.add_knowledge((pos[0],pos[1]-1),HC.N)
            if (pos[1]-2 >= 0):
                self.add_knowledge((pos[0],pos[1]-2),HC.N)
            if (pos[0]-1 >= 0):
                self.add_knowledge((pos[0]-1,pos[1]),HC.E)
            if (pos[0]-2 >= 0):
                self.add_knowledge((pos[0]-2,pos[1]),HC.E)


        pass

    def je_sais_pas_tt(self):
        #boolean pour savoir si notre dico est complet
        for i in range(self.n):
            for j in range(self.m):
                if not self.has_knowledge(i,j):
                    return True
                if self.knowledge[(i,j)] in [HC.N, HC.E, HC.S, HC.W]:
                    return True
        return False

    def get_liste_mur(self)->List[Tuple[int,int]]:
        """Retourne la liste des murs"""
        r = []
        for pos,val in self.knowledge:
            if val == HC.WALL:
                r.append(pos)
        return r
    
    def get_liste_casevu(self)->List[Tuple[int,int]]:
        """Retourne la liste des cases vues"""
        self.maj_vision_garde()
        r = []
        for pos,val in self.matrice_vision:
            if val != 0:
                r.append(pos)
        return r

    

def knowledge_to_clause_personne(Dico_know : Dict[Tuple[int, int], HC], dict_var_to_num : Dict[str, int])-> ClauseBase:
    r :ClauseBase =[]
    for i,v in Dico_know.items():
        #print(v)
        if v in [HC.CIVIL_E, HC.CIVIL_N, HC.CIVIL_S, HC.CIVIL_W, HC.GUARD_E, HC.GUARD_N, HC.GUARD_S, HC.GUARD_W]:
            #print(f"{i[0]}{i[1]}_P")
            r.append(dict_var_to_num[f"{i[0]}{i[1]}_P"]) # type: ignore
    return r


