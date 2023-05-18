from pprint import pprint
import random
from MatriceHitman import MatriceHitman

class Hitman:
    def __init__(self,m,n) -> None:
        self.position = (0, 0) # (i, j)
        self.matrice = MatriceHitman(m, n)
        self.orientation = "N"
        pass

    @property
    def get_position(self):
        return self.position

    def set_position(self, i, j):
        self.position = (i, j)
        pass

    @property
    def get_matrice(self):
        return self.matrice
    def set_matrice(self, matrice):
        self.matrice = matrice
        pass

    @property
    def get_orientation(self):
        return self.orientation
    def set_orientation(self, orientation):
        self.orientation = orientation
        pass
    
    def avancer_possible(self):
        #TODO on peut avancer si il n'y a pas de mur, ni de garde, ni de bordure de map.
        possible =["V","I"]
        if self.orientation == "N":
            if self.matrice.matrice[self.position[0]+1][self.position[1]] in possible:
                return True
            else:
                return False
        elif self.orientation == "S":
            if self.matrice.matrice[self.position[0]-1][self.position[1]] in possible:
                return True
            else:
                return False
        elif self.orientation == "E":
            if self.matrice.matrice[self.position[0]][self.position[1]+1] in possible:
                return True
            else:
                return False
        elif self.orientation == "O":
            if self.matrice.matrice[self.position[0]][self.position[1]-1] in possible:
                return True
            else:
                return False
        
        pass

    def avancer(self):
        print(f"Hitman est en {self.position} et regarde vers {self.orientation}")
        #la matrice est inversé ( le nord est en bas )
        if (self.avancer_possible()):
            if self.orientation == "N":
                self.position[0] += 1
            elif self.orientation == "S":
                self.position[0] -= 1
            elif self.orientation == "E":
                self.position[1] += 1
            elif self.orientation == "O":
                self.position[1] -= 1
        else:
            print("Deplacement impossible")
        pass

    def regarder_droite(self):
        if self.orientation == "N":
            self.orientation = "E"
        elif self.orientation == "E":
            self.orientation = "S"
        elif self.orientation == "S":
            self.orientation = "O"
        elif self.orientation == "O":
            self.orientation = "N"
        pass

    def regarder_gauche(self):
        if self.orientation == "N":
            self.orientation = "O"
        elif self.orientation == "O":
            self.orientation = "S"
        elif self.orientation == "S":
            self.orientation = "E"
        elif self.orientation == "E":
            self.orientation = "N"
        pass

    def get_info(self):
        #TODO arbitre nous donne les infos
        pass

    def action_random(self):
        nombre = random.randint(0, 3)
        if nombre == 0:
            self.avancer()
        elif nombre == 1:
            self.regarder_droite()
        elif nombre == 2:
            self.regarder_gauche()
        pass

    def tour(self):
        #On est sur une case on a des infos, on modifie nos connaissance, on choisit une action
        
        for i,j,val in get_info():
            self.matrice.ajout_connaissance(i,j,val)
        action_random()
        pass

def generer_matrice_aleatoire(m,n, nbr_G, nbr_I):
    elements = [" C "," D "]
    elements += [random.choice(["G_N", "G_O", "G_S", "G_E"]) for _ in range(nbr_G)]
    elements += [random.choice(["I_N", "I_O", "I_S", "I_E"]) for _ in range(nbr_G)]
    r = m*n - len(elements)
    elements += [random.choice([" V "," V "," M "]) for _ in range(r)]
    random.shuffle(elements)
    mat =[[elements.pop() for _ in range(n)] for _ in range(m)]
    return mat

def main():
    hitman = Hitman(3, 4)
    hitman.matrice.ajout_connaissance(0, 1, "G_N")
    hitman.matrice.ajout_connaissance(1, 1, "M")
    hitman.matrice.afficher_matrice()
    hitman.avancer()
    print(hitman.position)

    hitman.matrice.afficher_matrice()
    hitman.regarder_droite()
    hitman.avancer()
    print(hitman.position)

    hitman.regarder_droite()
    hitman.avancer()
    print(hitman.position)


    print("\n\n")
    matrice_aleatoire = generer_matrice_aleatoire(4,3, 1, 1)
    pprint(matrice_aleatoire)

    test =MatriceHitman(4,3)
    test.matrice = matrice_aleatoire
    test.afficher_matrice()
    pass

if __name__ == "__main__":
    main()