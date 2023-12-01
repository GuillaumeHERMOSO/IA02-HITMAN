import os
import time
from src.mouvement_phase1 import *
from src.a_etoile import *
from src.arbitre.hitman import *
from src.Class_HitmanKnowledge import *
from pprint import pprint
from src.sat import *
from src.clause_dynamique import *


def phase1(hr: HitmanReferee, sat=False, affichage=False, temp=0.5, cb_de_temp=True):
    if cb_de_temp:
        start = time.time()

    status = hr.start_phase1()
    n = status["n"]
    m = status["m"]

    # on cree la representation des connaissance de Hitman
    con = HitmanKnowledge(m=m, n=n)
    con.ajout_voir_knowledge(status)

    # on affiche la map
    if affichage:
        os.system("cls" if os.name == "nt" else "clear")
        afficher(con, hr, status)
        print(f"{status['position']} {status['orientation']} p :{status['penalties']}")

    # on applique la strategie de debut de partie
    if sat:
        clauses: ClauseBase = []
        list_cases = creer_list_var(m, n)
        dict_var_to_num, comp = creer_dictionnaire_cases_par_list(list_cases)
        clauses_pas_connaissance = []

    status = debut_map(hr, con)

    if affichage:
        sleep(temp)
        os.system("cls" if os.name == "nt" else "clear")
        afficher(con, hr, status)
        print(f"{status['position']} {status['orientation']} p :{status['penalties']}")

    s0 = status["position"]
    visited = [s0]

    while con.je_sais_pas_tt():
        # Tant que Hitman c'est pas tout
        s0 = status["position"]
        visited.append(s0)

        # on regarde les cases inconnus les plus proches
        liste = get_liste_case_inconnu_plus_proche_hitman(s0[0], s0[1], n, m, con)
        buts = []

        if sat:
            clauses_connaissance = knowledge_to_clause_personne(
                con.get_all_knowledge(), dict_var_to_num
            )
            clauses_pas_connaissance += ecouter(hr, dict_var_to_num)
            clauses = clauses_connaissance + clauses_pas_connaissance
            boucle_deduction2(dict_var_to_num, con, clauses, len(list_cases))

            if affichage:
                sleep(temp)
                os.system("cls" if os.name == "nt" else "clear")
                print()
                afficher(con, hr, status)
                print(
                    f"{status['position']} {status['orientation']} p :{status['penalties']}"
                )

        # tant qu'on a pas de destination on regarde si on peut voir une case inconnu
        while buts == []:
            # on prend la premiere case de la liste
            goal = liste.pop(0)
            # on regarde ou on peut aller pour voir la case
            buts, orientation_a_obtenir = case_connu_qui_peut_voir_une_case(
                goal, m, n, con.get_all_knowledge()
            )

        # on applique l'algorithme A* pour trouver le chemin
        s, d = astar_with_parent(
            s0,
            buts,
            succ,
            con.get_all_knowledge(),
            m,
            n,
            con.get_liste_mur(),
            con.get_liste_casevu(),
            visited,
        )
        oro = orientation_a_obtenir[s]

        # on reconstruit le chemin
        chemin = []
        while s != s0:
            chemin.append(s)
            s = d[s]
        chemin.append(s0)
        chemin.reverse()

        orientation = status["orientation"]

        # on transforme le chemin en liste d'action qu'on execute
        actions = chemin_to_action(chemin, orientation, con, hr)
        for a in actions:
            status = a()
            con.ajout_voir_knowledge(status)
            if sat:
                clauses_pas_connaissance += ecouter(hr, dict_var_to_num)
                pass

            if affichage:
                sleep(temp)
                os.system("cls" if os.name == "nt" else "clear")
                print(a.__name__)
                afficher(con, hr, status)
                print(
                    f"{status['position']} {status['orientation']} p :{status['penalties']}"
                )

        # on est sur une case nous permettant de voir la case inconnu, on tourne en sa direction
        tourner_action = tourner(status["orientation"], oro, hr)
        for a in tourner_action:
            status = a()
            con.ajout_voir_knowledge(status)
            if sat:
                # TODO mettre l'ecoute dans les clauses
                pass

            if affichage:
                sleep(temp)
                os.system("cls" if os.name == "nt" else "clear")
                print(a.__name__)
                afficher(con, hr, status)
                print(
                    f"{status['position']} {status['orientation']} p :{status['penalties']}"
                )

    if cb_de_temp:
        end = time.time()
        print(f"temps d'execution : {end - start}")
    # on a tout vu on envoie le contenu au main
    return con
