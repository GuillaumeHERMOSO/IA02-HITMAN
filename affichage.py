from clause_dynamique import *
from test_clause_hitman import *
from verite_sur_le_monde import *
Grid_str = List[List[str]]

#model de la forme [-1, -2, -3, ...,-141, -142, -143, -144, 145, -146]
# pour chaque case on a V","M","C","D","T","I","I_N","I_S","I_E","I_O","G","G_N","G_S","G_E","G_O","P"
# on a donc 16 variables par case
#on affiche la grille avec les lettres correspondantes sauf ["P","G","I"]

def model_to_grid(model: Model, n: int, m: int, list_var):
    nb = 0
    for i in range(m):
        for j in range(n):
            for tab in model[16*(i*n+j):16*(i*n+j+1)]:
                if tab > 0:
                    # affichage de la lettre coreespondante ex 00_G_N on afficher G_N
                    #print(list_var[tab],end="")
                    print(list_var[tab-1][3:],end="")
                    nb += 1
                    break
            print("    ",end="")
    print(f"\nNombre de cases remplies : {nb}")



def main():


    pass


if __name__ == "__main__":
    main()