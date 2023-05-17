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
    
    def deplacement_possible(self):
        #TODO on peut avancer si il n'y a pas de mur, ni de garde, ni de bordure de map.

        if self.orientation == "N":
            if self.position[0] == 0:
                return False
            elif self.matrice[self.position[0]-1][self.position[1]] in ["M","G","G_N","G_S","G_E","G_O"]:
                return False
            else:
                return True
        elif self.orientation == "S":
            if self.position[0] == self.matrice.nb_lignes-1:
                return False
            elif (self.matrice[self.position[0]+1][self.position[1]] in ["M","G","G_N","G_S","G_E","G_O"]):
                return False
            else:
                return True
        elif self.orientation == "E":
            if self.position[1] == self.matrice.nb_colonnes-1:
                return False
            elif self.matrice[self.position[0]][self.position[1]+1] in ["M","G","G_N","G_S","G_E","G_O"]:
                return False
            else:
                return True
        elif self.orientation == "O":
            if self.position[1] == 0:
                return False
            elif self.matrice[self.position[0]][self.position[1]-1] in ["M","G","G_N","G_S","G_E","G_O"]:
                return False
            else:
                return True
        pass

    def avancer(self):
        print(f"Hitman est en {self.position} et regarde vers {self.orientation}")
        if (self.deplacement_possible()):
            if self.orientation == "N":
                self.position[0] -= 1
            elif self.orientation == "S":
                self.position[0] += 1
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



def main():
    hitman = Hitman(3, 4)
    hitman.matrice.ajout_connaissance(0, 1, "G_N")
    hitman.matrice.ajout_connaissance(1, 1, "M")
    hitman.matrice.afficher_matrice()
    hitman.avancer()
    hitman.matrice.afficher_matrice()
    hitman.regarder_droite()
    hitman.avancer()
    hitman.matrice.afficher_matrice()
    pass

if __name__ == "__main__":
    main()