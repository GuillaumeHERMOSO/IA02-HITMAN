class MatriceHitman:
    def __init__(self, nb_lignes, nb_colonnes):
        self.matrice = [[" x " for _ in range(nb_colonnes)] for _ in range(nb_lignes)]
        self.nb_lignes = nb_lignes
        self.nb_colonnes = nb_colonnes
        pass
    
    def afficher_matrice(self):
        print()
        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                print(self.matrice[i][j], end=" ")
            print()
        pass
    
    def ajout_connaissance(self, i, j, lettre):
        if (0 <= i < self.nb_lignes and 0 <= j < self.nb_colonnes):
            if len(lettre) == 3:
                self.matrice[i][j] = lettre
            elif len(lettre) == 1:
                self.matrice[i][j] = " " + lettre + " "
            else:
                print("La lettre doit avoir 3 caractères ou une taille de 1.")
        else:
            print("Position invalide !")
        pass
    def __str__(self) -> str:
        p ="\n"
        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                p += self.matrice[i][j] + " "
            p += "\n"
        return p



def main():
    matrice_vide = MatriceHitman(3, 4)
    #matrice_vide.afficher_matrice()
    matrice_vide.ajout_connaissance(0, 1, "G_N")
    matrice_vide.ajout_connaissance(1, 1, "M")
    matrice_vide.afficher_matrice()

    pass


if __name__ == "__main__":
    main()