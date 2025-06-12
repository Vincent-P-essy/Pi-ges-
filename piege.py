#!/usr/bin/env python3

# Concept : 
# - Donjon : action par tour, manipule des salles
# - Salles : passages vers des directions cardinales, contiennent des dragons
# - Dragons : plusieurs niveaux, tous différents
#
# - Aventurier : déplacement tour par tour de salle en salle vers l'intention
# - Intention : cible le dragon le plus fort accessible (orgueil)
#
# Doc FLTK : https://antoinemeyer.frama.io/fltk/
import random, fltk, time, os, importlib, time
import game

## VARIABLES DE CONFIGURATION
LARGEUR_FENETRE = 900
HAUTEUR_FENETRE = 900
OFFSET_X = 230
OFFSET_Y = 100

DIM = game.DIM
VERTICAL = game.VERTICAL
HORIZONTAL = game.HORIZONTAL

PLACEMENT=0
TIRETTES=1
FIN=2

def run_game(joueur1, joueur2, plateau):
    """
    Running game
    @params joueur1, joueur2, players (class Joueur)
            plateau, game board (class Plateau)
    @return void
    """

    # A variable that allows to store/check the current phase during the game
    gamephase = PLACEMENT

    retry = False

    # Current player (XXX, joueur1 commence toujours)
    currentplayer = joueur1
    nextplayer = joueur2
    gagnant = None

    fltk.cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)
    fltk.texte(LARGEUR_FENETRE/2, HAUTEUR_FENETRE/20,
                "Pièges",
                couleur="black",
                taille=30,
                ancrage='center')

    modeles = {
        "tirette_horiz":"sprites/tirette.png",
        "barre_horiz":"sprites/barre.png",
        "tirette_vert":"sprites/tirette2.png",
        "barre_vert":"sprites/barre2.png",
        "bille1":"sprites/bille1.png",
        "bille2":"sprites/bille2.png",
        "tour_de_plateau":"sprites/bois3.png",
        "case1":"sprites/bois1.png",
        "case2":"sprites/bois2.png",
        "trou": "sprites/trou.png",
        "trou_horiz": "sprites/trou_partiel1.png",
        "trou_vert": "sprites/trou_partiel2.png"
    }

    # Boucle principale

    while gamephase != FIN:
        if not retry:
            # inversion des rôles
            currentplayer, nextplayer = nextplayer, currentplayer

            if currentplayer is joueur1:
                strjoueur = "joueur1"
            elif currentplayer is joueur2:
                strjoueur = "joueur2"

            if gamephase == PLACEMENT:
                strphase = "placement des billes"
            elif gamephase == TIRETTES:
                strphase = "manipulation des tirettes, \nclic droit pour pousser, clic gauche pour tirer"

            fltk.efface("joueur")
            fltk.texte(LARGEUR_FENETRE/2, HAUTEUR_FENETRE/10,
                    "Phase {} : au tour du {}".format(strphase, strjoueur),
                    couleur="green",
                    taille=20,
                    ancrage='center',
                    tag="joueur")

        retry = True

        # Affichage plateau
        # Tirettes verticales
        for i in range(DIM):
            n = plateau.tirettes[0][i].position

            fltk.efface("tv{}".format(i))
            fltk.image( OFFSET_X + (i+1)*62,
                        OFFSET_Y + (DIM+1)*62 + n*30,
                        modeles["tirette_vert"],
                        ancrage = "center",
                        largeur=50,
                        hauteur=50,
                        tag="tv{}".format(i))

            for x in range(n):
                fltk.image( OFFSET_X + (i+1)*62,
                            OFFSET_Y + (DIM+1)*62 + x*30,
                            modeles["barre_vert"],
                            ancrage = "center",
                            largeur=50,
                            hauteur=50,
                            tag="tv{}".format(i))

        # Tirettes horizontales
        for j in range(DIM):
            #XXX récupérer la position de la tirette -> n
            #    boucler x fois pour afficher des barres
            n = plateau.tirettes[1][j].position

            fltk.efface("th{}".format(j))
            fltk.image( OFFSET_X + 20 + (0)*62 - n*30,
                        OFFSET_Y + 20 + (j+1)*62,
                        modeles["tirette_horiz"],
                        ancrage = "center",
                        largeur=55,
                        hauteur=55,
                        tag="th{}".format(j))

            for x in range(n):
                fltk.image( OFFSET_X + 20 + (0)*62 - x*30,
                            OFFSET_Y + 20 + (j+1)*62,
                            modeles["barre_horiz"],
                            ancrage = "center",
                            largeur=50,
                            hauteur=50,
                            tag="th{}".format(j))

        # Plateau
        for i in range(0,DIM):
            for j in range(0,DIM):

                # Choix du type de sprite selon position
                if (i+j) % 2 == 0:
                    type_modele = "case1"
                else:
                    type_modele = "case2"

                fltk.image( OFFSET_X + 2  + (i+1)*62,
                            OFFSET_Y + 20 + (j+1)*62,
                            modeles[type_modele],
                            ancrage = "center",
                            largeur=60,
                            hauteur=60,
                            tag="{},{}".format(i,j))

                potentiel_trou = plateau.est_ce_un_trou(i,j)
                #print(potentiel_trou)
                if potentiel_trou > -1:
                    if potentiel_trou == 2:
                        modele_trou = modeles["trou"]
                    elif potentiel_trou == HORIZONTAL:
                        modele_trou = modeles["trou_horiz"]
                    elif potentiel_trou == VERTICAL:
                        modele_trou = modeles["trou_vert"]

                    fltk.image( OFFSET_X + 2  + (i+1)*62,
                                OFFSET_Y + 20 + (j+1)*62,
                                modele_trou,
                                ancrage = "center",
                                largeur=60,
                                hauteur=60,
                                tag="{},{}".format(i,j))

        # Billes
        for bille in plateau.mise_à_jour():
            x,y = bille[0], bille[1]
            fltk.efface("b{},{}".format(x,y))

        for bille in plateau.billes:
            if bille[2] is joueur1:
                fltk.image( OFFSET_X + 2  + (bille[0]+1)*62,
                            OFFSET_Y + 20 + (bille[1]+1)*62,
                            modeles["bille1"],
                            ancrage = "center",
                            largeur=30,
                            hauteur=30,
                            tag="b{},{}".format(i,j))

            if bille[2] is joueur2:
                fltk.image( OFFSET_X + 2  + (bille[0]+1)*62,
                            OFFSET_Y + 20 + (bille[1]+1)*62,
                            modeles["bille2"],
                            ancrage = "center",
                            largeur=30,
                            hauteur=30,
                            tag="b{},{}".format(i,j))


        if gamephase == TIRETTES and currentplayer.compte == 0:
            gagnant = nextplayer
            gamephase = FIN

            if currentplayer is joueur1:
                strjoueur = "joueur2"
            elif currentplayer is joueur2:
                strjoueur = "joueur1"

            fltk.efface("joueur")
            fltk.texte(LARGEUR_FENETRE/2, HAUTEUR_FENETRE/10,
                    "Le joueur {} a gagné !".format(strjoueur),
                    couleur="red",
                    taille=20,
                    ancrage='center',
                    tag="joueur")


        fltk.mise_a_jour()
        event = fltk.attend_ev()

        if "Quitte" in fltk.type_ev(event):
            for i in range(DIM):
                for j in range(DIM):
                    fltk.efface("{},{}".format(i,j))
            fltk.ferme_fenetre()
            return

        if "Touche" in fltk.type_ev(event) and "Escape" in fltk.touche(event):
            for i in range(DIM):
                for j in range(DIM):
                    fltk.efface("{},{}".format(i,j))
            fltk.ferme_fenetre()
            return

        if "ClicGauche" in fltk.type_ev(event):
            # XXX à améliorer
            x = fltk.abscisse(event)
            y = fltk.ordonnee(event)

            #print("Clic sur coords ({},{})".format(x,y))

            if gamephase == PLACEMENT:
                i =  int( (x - OFFSET_X - 2 + 62/2)/62 - 1)
                j = int( (y - OFFSET_Y - 20 + 62/2)/62 - 1)

                if i<DIM and j<DIM and i>=0 and j>=0:
                    retry = not currentplayer.placer_bille([nextplayer], i,j)

                if len(plateau.billes) == 10:
                    gamephase = TIRETTES

            elif gamephase == TIRETTES:
                # XXX
                i =  int( (x - OFFSET_X - 2 + 62/2)/62 - 1)
                j = int( (y - OFFSET_Y - 20 + 62/2)/62 - 1)


                if i<DIM and j>=DIM-1 and i>=0 and j>=0:
                    print("     tirette {}".format(i))
                    retry = not plateau.tirettes[VERTICAL][i].tirer()

                if i<DIM and j<DIM and i<=0 and j>=0:
                    print("     tirette {}".format(j))
                    retry = not plateau.tirettes[HORIZONTAL][j].tirer()

        if "ClicDroit" in fltk.type_ev(event):
            # XXX à améliorer
            x = fltk.abscisse(event)
            y = fltk.ordonnee(event)

            #print("Clic sur coords ({},{})".format(x,y))

            if gamephase == TIRETTES:
                # XXX
                i =  int( (x - OFFSET_X - 2 + 62/2)/62 - 1)
                j = int( (y - OFFSET_Y - 20 + 62/2)/62 - 1)


                if i<DIM and j>=DIM-1 and i>=0 and j>=0:
                    print("     tirette {}".format(i))
                    retry = not plateau.tirettes[VERTICAL][i].pousser()

                if i<DIM and j<DIM and i<=0 and j>=0:
                    print("     tirette {}".format(j))
                    retry = not plateau.tirettes[HORIZONTAL][j].pousser()


## Fonction principale
def main():
    importlib.reload(fltk) # corrige un bug sérieux de fltk avec les images

    plateau = game.Plateau()

    joueur1 = game.Joueur(plateau)
    joueur2 = game.Joueur(plateau)

    run_game(joueur1, joueur2, plateau)
    time.sleep(5)
    return 0

main()
