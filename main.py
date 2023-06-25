from typing import List, Tuple
from src.arbitre.hitman import *
from src.Class_HitmanKnowledge import *
from src.arbitre.hitman import HC
from src.mouvement_phase1 import *
from src.a_etoile import *
from src.phase2 import *
from src.sat import *
from src.phase1 import *
from src.contraintes import *
from src.clause_dynamique import *


def main_phase1() -> None:
    """ Fonction qui permet de lancer que la phase 1"""
    hr = HitmanReferee()
    con = phase1(hr,affichage=False, sat =True)
    status = hr.send_content(con.get_all_knowledge())
    status = hr.end_phase1()
    pprint(status)
    pass


def main_phase2() -> None:
    """ Fonction qui permet de lancer que la phase 2"""
    hr = HitmanReferee()
    status = hr.start_phase1()
    n = status["n"]
    m = status["m"]
    con = HitmanKnowledge(m=m, n=n)
    status = hr.send_content(con.get_all_knowledge())
    status = hr.end_phase1()
    con.knowledge = status[3]

    hr.start_phase2()
    phase2(hr,con,affichage=True)

def main_phase1_2() -> None:
    """ Fonction qui permet de lancer la phase 1 et la phase 2"""
    hr = HitmanReferee()
    status = hr.start_phase1()

    temp = 0.3
    con = phase1(hr, affichage=True, temp=temp)
    status = hr.send_content(con.get_all_knowledge())
    status = hr.end_phase1()

    con.knowledge = status[3]
    phase2(hr,con,affichage=True, temp=temp)

    #fini


if __name__ == "__main__":
    #main_phase1()
    #main_phase2()
    main_phase1_2()
