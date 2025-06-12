#!/usr/bin/env python3

##### Principes généraux du jeu de piege:
# Partie preliminaire:
# Au début de la partie, les joueurs placent les tirettes dans des positions aléatoires.
# Ensuite, chacun à leur tour, ils placent une bille sur la grille, aux endroits où il
# n’y a pas de trou. Lorsque toutes les billes sont placées, le jeu peu commencer.
#
# Partie:
# Le jeu se joue au tour par tour. À son tour, un joueur choisit une tirette et
# la déplace d’un cran dans le sens qu’il souhaite dans le but de faire tomber les
# billes des joueurs adverses.
# Le gagnant est le dernier joueur à avoir des billes en jeu.
# structures de données:
#   • La position des billes sur la grille
#       - liste des billes (tuples x,y)
#
#   • La position des tirettes et la position de leurs trous
#       - liste des tirettes (avec la tirette 0 en bas à gauche)
#           - une tirette est une liste contenant un nombre (la position)
#       - liste des cases pour les tirettes (taille 7×7) (O(1))
#            - lorsque trou True
#            - sinon false False
#
# Il vous faudra ensuite implémenter les fonctions de base du moteur du jeu :
#   • Une fonction qui déplace une tirette
#   • Une fonction qui met à jour les positions des billes, en faisant tomber les
# billes situées au-dessus de trous
#   • Une fonction qui génère aléatoirement une tirette, avec au moins un trou (sinon on ne peut pas gagner !)
#   • Une fonction qui permet de placer une bille d’un joueur sur la grille (pour la phase préliminaire)
#
#   ▬ ▬ ▬ ▬ ▬ ▬ ▬
#   ―――――――――――――
#  |❍|❍|❍|❍|❍|❍|❍|▬
#  |❍|❍|❍|❍|❍|❍|❍|▬
#  |❍|❍|❍|❍|❍|❍|❍|▬
#  |❍|❍|❍|❍|❍|❍|❍|▬
#  |❍|❍|❍|❍|❍|❍|❍|▬
#  |❍|❍|❍|❍|❍|❍|❍|▬
#  |❍|❍|❍|❍|❍|❍|❍|▬
#   ―――――――――――――
#   | | | | | | |
#   | | | | | | |
#   | | | | | | |
#   ▬ ▬ ▬ ▬ ▬ ▬ ▬

import random

DIM = 7
VERTICAL = 0
HORIZONTAL = 1

def calcul_coord(x,y):
    """
    calcule une nouvelle coordonnée
    @params void
    @return une nouvelle position
    """

    #print("COORD : x={}, y={}, res = {}".format(x, y, y * DIM + x))

    return y * DIM + x


class Plateau:
    def __init__(self):
        """
        constructor
        """

       # Espace 7 × 7, deux fois pour
       # vertical et horizontal
        self.trous = [ [False] * DIM * DIM, [False] * DIM * DIM ]

        self.billes = []                          # liste de tuples (x,y,joueur)

        # Espace 7 , deux fois pour
        # vertical et horizontal
        self.tirettes = [ [None] * DIM, [None] * DIM ]

        self.générer_tirettes()

    def générer_tirettes(self):
        """
        genere les tirettes 
        @params void
        @return void
        
        """
        for orientation in range(2): # vertical et horizontal
            for i in range(DIM):
                tirette = Tirette(i+(orientation*DIM), self, orientation=orientation)
                for trou in tirette.trous:
                    self.trous[orientation][tirette.calcul_pos(trou)] = True
                self.tirettes[orientation][i] = tirette

        print("Liste trous communs")
        liste=[]
        for i in range(DIM):
            for j in range(DIM):
                if  self.trous[HORIZONTAL][i + j * DIM] and \
                    self.trous[VERTICAL][i + j * DIM]:
                        print("({}, {})".format(i,j))
                        liste.append((i,j))

        print("Liste trous partiels horizontaux")
        for i in range(DIM):
            for j in range(DIM):
                if  self.trous[HORIZONTAL][i + j * DIM] and (i,j) not in liste:
                        print("({}, {})".format(i,j))

        print("Liste trous partiels verticaux")
        for i in range(DIM):
            for j in range(DIM):
                if  self.trous[VERTICAL][i + j * DIM] and (i,j) not in liste:
                        print("({}, {})".format(i,j))

    def est_ce_un_trou(self,x,y):
        """
        la methode renvoie True si c'est un Trou , False sinon
        @params x l'abscisse et y l'ordonnée
        @return VERTICAL, si VERTICAL a un trou
                HORIZONTAL, si HORIZONTAL a un trou
                2, si trou aligné
                0, si aucun trou
        """
        if  self.trous[VERTICAL][calcul_coord(x,y)] and \
            self.trous[HORIZONTAL][calcul_coord(x,y)]:
                return 2
        elif self.trous[VERTICAL][calcul_coord(x,y)]:
            return VERTICAL
        elif self.trous[HORIZONTAL][calcul_coord(x,y)]:
            return HORIZONTAL
        else:
            return -1


    def mise_à_jour(self):
        """
        la methode enleve le tuple de coordonnées (x,y) correspondant a la bille dans la liste self.billes
        si il y a un trou a ces coordonnées
        @params self
        @return void
        """
        L = []
        for bille in self.billes:
            if self.est_ce_un_trou(bille[0], bille[1]) == 2:
                x, y = bille[0], bille[1]
                bille[2].compte -= 1
                self.billes.remove(bille)
                L.append((x,y))
        return L

class Tirette:
    def __init__(self, numéro, plateau, orientation=random.randint(0,1), trous=[]):
        """
        Constructor
        """
        self.numéro = numéro            # définit son placement dans l'espace
        #print("Tirette n°{}".format(self.numéro))
        
        self.plateau = plateau          # lien vers le plateau de jeu

        self.orientation = orientation  # 0 pour vertical, 1 pour horizontal

        self.trous = []                 # liste de trous sous la forme d'un offset 
                                        # du point 0 de la tirette (bas ou gauche selon 
                                        # orientation)

        # position initiale à 0
        self.position = 0

        # Si rien fourni, générer 50% de trous
        if len(self.trous) == 0:
            for i in range(DIM):
                
                tirage = random.random() * 100
                
                if (tirage < 65):
                    self.trous.append(i)

        print("Tirette n°{} a les trous : {}".format(self.numéro, self.trous))

    def calcul_pos(self, offset):
        """
        la methode calcule les coordonnées de la tirette selon l'orientation de la tirette
        @params offset
        @return coordonnées
        """
        
        if self.orientation == VERTICAL:
            return calcul_coord(self.numéro, offset - self.position)
        elif self.orientation == HORIZONTAL:
            return calcul_coord(offset - self.position, self.numéro - DIM)
        else:
            raise()

    def déplacer(self, nouvelle_position):
        """
        La methode enleve le trou d'origine et rajoute un trou lorsqu'on déplace la Tirette
        @params nouvelle_position
        @return boolean 
        """
        # Ancienne position de la tirette
        ancienne_position = self.position
        
        # Pour chaque trou de la tirette
        for trou in self.trous:
            
            # Nettoie l'ancienne position du trou si dans le plateau
            if trou - self.position > 0: 
                self.plateau.trous[self.orientation][self.calcul_pos(trou)] = False
            
            # Met à jour la position du trou dans l'espace si dans le plateau 
            if trou + (nouvelle_position - ancienne_position) < DIM:
                self.plateau.trous[self.orientation][self.calcul_pos(trou +
                                (nouvelle_position - ancienne_position))] = True

        # Mise à jour de la position de la tirette
        self.position = nouvelle_position

    def pousser(self):
        if self.position > 0:
            self.déplacer(self.position - 1)
            return True
        return False

    def tirer(self):
        if self.position < 3:
            self.déplacer(self.position + 1)
            return True
        return False

class Joueur:
    def __init__(self, plateau):
        """
        constructor
        """
        self.plateau = plateau

        self.compte = 0

    def placer_bille(self, nextplayers, x, y):
        """
        la methode verifie si il n'y a pas de trou et de billes aux coordonnées du tuple (x,y)
        @params (x,y) coordonnées
        @return boolean
        
        """
        if not self.plateau.est_ce_un_trou(x,y) == 2:
            if not (x,y,self) in self.plateau.billes:
                for nextplayer in nextplayers:
                    if (x,y,nextplayer) in self.plateau.billes:
                        return False
                self.plateau.billes.append((x,y,self))
                self.compte += 1
                return True
        return False
