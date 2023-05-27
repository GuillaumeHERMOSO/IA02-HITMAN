from enum import Enum
from typing import Tuple, Dict

class HC(Enum): 
    EMPTY = 1
    WALL = 2
    GUARD_N = 3
    GUARD_E = 4
    GUARD_S = 5
    GUARD_W = 6
    CIVIL_N = 7
    CIVIL_E = 8
    CIVIL_S = 9
    CIVIL_W = 10
    TARGET = 11
    SUIT = 12
    PIANO_WIRE = 13
    N = 14
    E = 15
    S = 16
    W = 17

class HitmanKnowledge:
    def __init__(self, m: int, n: int):
        self.m = m
        self.n = n
        self.knowledge = {}

    def add_knowledge(self, position: Tuple[int, int], content: HC):
        self.knowledge[position] = content

    def get_knowledge(self, position: Tuple[int, int]) -> HC:
        return self.knowledge.get(position, HC.EMPTY)

    def get_all_knowledge(self) -> Dict[Tuple[int, int], HC]:
        return self.knowledge

    def has_knowledge(self, i: int, j: int) -> bool:
        return (i, j) in self.knowledge
    

    def __str__(self) -> str:
        """Affichage de la matrice de connaissance avec 0,0 en bas à gauche et m,n en haut à droite, si il y a rien on affiche x"""
        r =""
        for i in reversed(range(self.m)):
            for j in range(self.n):
                if self.has_knowledge(i,j):
                    #format permet d'avoir la meme taille pour chaque case  max 10 caractere, ^ pour centrer
                    r += format(self.get_knowledge((i,j)).name,"^7") +" "
                    
                else:
                    r += format("x","^7") +" "
            r +="\n"
        return r

