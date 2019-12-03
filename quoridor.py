""" Main du programme Jeu Quorridor - Phase 2
Écrit par :
Maxime Carpentier
Vincent Bergeron
Ousmane Touré
Le 2 décembre 2019
Ce programme contient la classe avec toutes
les méthodes pour jouer au jeu Quoridor
"""


import networkx as nx


class Quoridor:
    """
    Classe Quoridor, contient toutes les fonctions nécéssaires pour 
    jouer au jeu Quoridor.
    """
    def __init__(self, joueurs, murs=None):
        """
        Initialiser une partie de Quoridor avec les joueurs et les murs spécifiés,
        en s'assurant de faire une copie profonde de tout ce qui a besoin d'être copié.

        :param joueurs: un itérable de deux joueurs dont le premier est toujours celui qui
        débute la partie. Un joueur est soit une chaîne de caractères soit un dictionnaire.
        Dans le cas d'une chaîne, il s'agit du nom du joueur. Selon le rang du joueur dans
        l'itérable, sa position est soit (5,1) soit (5,9), et chaque joueur peut initialement
        placer 10 murs. Dans le cas où l'argument est un dictionnaire, celui-ci doit contenir
        une clé 'nom' identifiant le joueur, une clé 'murs' spécifiant le nombre de murs qu'il
        peut encore placer, et une clé 'pos' qui spécifie sa position (x, y) actuelle.

        :param murs: un dictionnaire contenant une clé 'horizontaux' associée à la liste des
        positions (x, y) des murs horizontaux, et une clé 'verticaux' associée à la liste des
        positions (x, y) des murs verticaux. Par défaut, il n'y a aucun murs placé sur le jeu.

        :raises QuoridorError: si l'argument 'joueurs' n'est pas itérable.
        :raises QuoridorError: si l'itérable de joueurs en contient plus de deux.
        :raises QuoridorError: si le nombre de murs qu'un joueur peut placer est >10, ou négatif.
        :raises QuoridorError: si la position d'un joueur est invalide.
        :raises QuoridorError: si l'argument 'murs' n'est pas un dictionnaire lorsque présent.
        :raises QuoridorError: si le total des murs placés et plaçables n'est pas égal à 20.
        :raises QuoridorError: si la position d'un murs est invalide.
        """
        # On vérifie si joueur est itérable, si invalide on soulève une erreur
        if not isinstance(joueurs, list):
            raise QuoridorError
        # On vérifie le nombre de joueur, si invalide on soulève une erreur
        if len(joueurs) > 2:
            raise QuoridorError
        # On différencie si c'est une chaine de charactère ou un dictionnaire
        # et on initialise les paramètres dans un dictionnaire en fonction
        if isinstance(joueurs[0], str):
            # Charactère donc nouvelle partie
            self.joueur1 = {'nom' : joueurs[0], 'murs' : 10, 'pos' : (5, 1)}
            self.joueur2 = {'nom' : joueurs[1], 'murs' : 10, 'pos' : (5, 9)}
        elif isinstance(joueurs[0], dict):
            # Dictionnaire donc partie en cours
            self.joueur1 = {'nom' : joueurs[0]['nom'],
                            'murs' : joueurs[0]['murs'],
                            'pos' : joueurs[0]['pos']}
            self.joueur2 = {'nom' : joueurs[1]['nom'],
                            'murs' : joueurs[1]['murs'],
                            'pos' : joueurs[1]['pos']}
        # Si un joueur à un nombre de murs invalide on soulève une erreur
        if ((self.joueur1['murs'] < 0) or (self.joueur1['murs'] > 10) or
                (self.joueur2['murs'] < 0) or (self.joueur2['murs'] > 10)):
            raise QuoridorError
        # On vérifie la position des joueurs, si invalide on soulève une erreur
        if (not 1 <= self.joueur1['pos'][0] <= 9 or
                not 1 <= self.joueur1['pos'][1] <= 9 or
                not 1 <= self.joueur2['pos'][0] <= 9 or
                not 1 <= self.joueur2['pos'][1] <= 9):
            raise QuoridorError
        # On vérifie le type de murs, si invalide on soulève une erreur
        if ((murs is not None) and not isinstance(murs, dict)):
            raise QuoridorError
        # Si il y a des murs, on enregistre leurs positions
        if murs is not None:
            self.verticaux = murs['verticaux']
            self.horizontaux = murs['horizontaux']
        else:
            self.verticaux = []
            self.horizontaux = []

        # On vérifie la position des murs verticaux,
        # si invalide on soulève une erreur
        for i in self.verticaux:
            if (not 2 <= i[0] <= 9 or
                    not 1 <= i[1] <= 8):
                raise QuoridorError
        # On vérifie la position des murs horizontaux,
        # si invalide on soulève une erreur
        for i in self.horizontaux:
            if (not 1 <= i[0] <= 8 or
                    not 2 <= i[1] <= 9):
                raise QuoridorError

        # On vérifie le nombre de murs en jeu, si invalide on soulève une erreur
        if ((murs is not None) and (len(self.verticaux) + len(self.horizontaux)
                                    + self.joueur1['murs']
                                    + self.joueur2['murs'] != 20)):
            raise QuoridorError
        elif ((murs is None) and (self.joueur1['murs']
                                  + self.joueur2['murs'] != 20)):
            raise QuoridorError


    def __str__(self):
        """
        Produire la représentation en art ascii correspondant à l'état actuel de la partie.
        Cette représentation est la même que celle du TP précédent.

        :returns: la chaîne de caractères de la représentation.
        """
        # On commence la chaine sous forme de liste avec la première ligne
        chaine = 3*[' '] + 35*['-'] + [' \n']
        # On remplis toutes les lignes du milieu
        for i in range(9, 0, -1): # On compte à l'envers pour placer bien les y
            chaine += str(i) + ' | ' + 8*'.   ' + '. |'
            if i != 1:
                chaine += '\n  |' + 34 * ' ' + ' |\n'
        # On met la ligne de la limite du damier
        chaine += '\n--|' + 35*'-' + '\n  | '
        # On met la ligne avec les nombres horizontaux (x)
        for i in range(1, 10):
            chaine += str(i) + '   '

        # On lit la liste des murs horizontaux
        for j in self.horizontaux:
            # Il y a 6 caractères pour les murs horizontaux donc on les place
            for i in range(7):
                chaine[42+ (19 - j[1]*2)*40 + 4*(j[0]-1)+i] = '-'

        # On lit la liste des murs verticaux
        for x in self.verticaux:
            # Il y a 3 caractères pour les murs verticaux donc on les place
            for y in range(3):
                chaine[35 + (16 - x[1]*2 + y)*40 + 4*(x[0]-1)+6] = '|'

        # On lit et on place le joueur 1
        chaine[37 + (16 - self.joueur1['pos'][1]*2+2)*40 +
               4*(self.joueur1['pos'][0]-1)+6] = '1'

        # On lit et on place le joueur 2
        chaine[37 + (16 - self.joueur2['pos'][1]*2+2)*40 +
               4*(self.joueur2['pos'][0]-1)+6] = '2'

        # On retourne la chaine de caractère en ajoutant la légende et en
        # faisant un join() sur la liste. On sépare en trois fois pour ne pas
        # dépasser la colonne 80
        legende = 'Légende: 1=' + str(self.joueur1['nom'])
        legende = legende + ', 2=' + str(self.joueur2['nom'])
        return  legende +'\n' + ''.join(chaine)


    def déplacer_jeton(self, joueur, position):
        """
        Pour le joueur spécifié, déplacer son jeton à la position spécifiée.

        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        :param position: le tuple (x, y) de la position du jeton (1<=x<=9 et 1<=y<=9).
        :raises QuoridorError: si le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: si la position est invalide (en dehors du damier).
        :raises QuoridorError: si la position est invalide pour l'état actuel du jeu.
        """
        # On vérifie si le numéro de joueur est valide, sinon on soulève
        # une erreur
        if joueur not in [1, 2]:
            raise QuoridorError

        # On vérifie si la position est valide, sinon on soulève une erreur
        if (not 1 <= position[0] <= 9 or not 1 <= position[1] <= 9 or
                not 1 <= position[0] <= 9 or not 1 <= position[1] <= 9):
            raise QuoridorError

        # On enregistre l'état de la partie, et on fait un graphe
        état = Quoridor.état_partie(self)
        graphe = construire_graphe(
            [joueur['pos'] for joueur in état['joueurs']],
            état['murs']['horizontaux'],
            état['murs']['verticaux'])

        # On vérfie le joueur sélectionné et si le coup est possible on le joue
        if joueur == 1:
            # Liste des coups possible
            possi = list(graphe.successors(self.joueur1['pos']))
            for i in possi:
                # Si notre coup est dans la liste on le joue
                if position == i:
                    self.joueur1['pos'] = position
            # Si on n'a pas joué de coup on soulève une erreur car la pos est
            # invalide
            if self.joueur1['pos'] != position:
                raise QuoridorError
        elif joueur == 2:
            # Liste des coups possible
            possi = list(graphe.successors(self.joueur2['pos']))
            for i in possi:
                # Si notre coup est dans la liste on le joue
                if position == i:
                    self.joueur2['pos'] = position
            # Si on n'a pas joué de coup on soulève une erreur car la pos est
            # invalide
            if self.joueur2['pos'] != position:
                raise QuoridorError



    def état_partie(self):
        """
        Produire l'état actuel de la partie.

        :returns: une copie de l'état actuel du jeu sous la forme d'un dictionnaire:
        {
            'joueurs': [
                {'nom': nom1, 'murs': n1, 'pos': (x1, y1)},
                {'nom': nom2, 'murs': n2, 'pos': (x2, y2)},
            ],
            'murs': {
                'horizontaux': [...],
                'verticaux': [...],
            }
        }

        où la clé 'nom' d'un joueur est associée à son nom, la clé 'murs' est associée
        au nombre de murs qu'il peut encore placer sur ce damier, et la clé 'pos' est
        associée à sa position sur le damier. Une position est représentée par un tuple
        de deux coordonnées x et y, où 1<=x<=9 et 1<=y<=9.

        Les murs actuellement placés sur le damier sont énumérés dans deux listes de
        positions (x, y). Les murs ont toujours une longueur de 2 cases et leur position
        est relative à leur coin inférieur gauche. Par convention, un murs horizontal se
        situe entre les lignes y-1 et y, et bloque les colonnes x et x+1. De même, un
        murs vertical se situe entre les colonnes x-1 et x, et bloque les lignes y et y+1.
        """
        # On retourne simplement l'état de la partie dans un dictionnaire
        return {'joueurs' : [self.joueur1, self.joueur2], 'murs' :
                {'horizontaux' : self.horizontaux, 'verticaux' : self.verticaux}}

    def jouer_coup(self, joueur):
        """
        Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel
        de la partie. Ce coup est soit le déplacement de son jeton, soit le placement d'un
        murs horizontal ou vertical.
        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        :raises QuoridorError: si le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: si la partie est déjà terminée.
        """
        # On vérifie si la partie est terminée, ou si le numéro de joueur est
        # mauvais, si c'est le cas on soulève une erreur
        if joueur not in [1, 2] or self.partie_terminée():
            raise QuoridorError

        # On créé le graphe pour pouvoir tester les positions possibles
        état = Quoridor.état_partie(self)
        graphe = construire_graphe(
            [joueur['pos'] for joueur in état['joueurs']],
            état['murs']['horizontaux'],
            état['murs']['verticaux']
        )

        # Si on avait sélectionné le joueur 1, on le place à la meilleure
        # position possible
        if (joueur == 1 and nx.has_path(graphe, (self.joueur1["pos"][0],
                                                 self.joueur1["pos"][1]),
                                        'B1')):
            self.joueur1["pos"] = nx.shortest_path(graphe,
                                                   (self.joueur1["pos"][0],
                                                    self.joueur1["pos"][1]),
                                                   'B1')[1]

        # Si on avait sélectionné le joueur 2, on le place à la meilleure
        # position possible
        if (joueur == 2 and nx.has_path(graphe, (self.joueur2["pos"][0],
                                                 self.joueur2["pos"][1]),
                                        'B2')):
            self.joueur2["pos"] = nx.shortest_path(graphe,
                                                   (self.joueur2["pos"][0],
                                                    self.joueur2["pos"][1]),
                                                   'B2')[1]


    def partie_terminée(self):
        """
        Déterminer si la partie est terminée.
        :returns: le nom du gagnant si la partie est terminée; False autrement.
        """
        # On vérifie si le joueur 1 ou 2 sont à la dernière position,
        # si c'est le cas on retourne le nom du joueur. Sinon on retourne False
        if self.joueur1['pos'][1] == 9:
            return self.joueur1['nom']

        if self.joueur2['pos'][1] == 1:
            return self.joueur2['nom']
        
        if (self.joueur1['pos'][1] != 9 and self.joueur2['pos'][1] != 1):
            return False

    def placer_mur(self, joueur, position, orientation):
        """
        Pour le joueur spécifié, placer un murs à la position spécifiée.
        :param joueur: le numéro du joueur (1 ou 2).
        :param position: le tuple (x, y) de la position du murs.
        :param orientation: l'orientation du murs ('horizontal' ou 'vertical').
        :raises QuoridorError: si le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: si un murs occupe déjà cette position.
        :raises QuoridorError: si la position est invalide pour cette orientation.
        :raises QuoridorError: si le joueur a déjà placé tous ses murs.
        """
        # On vérifie si le numéro de joueur est valide, sinon on
        # soulève une erreur
        if joueur not in [1, 2]:
            raise QuoridorError
        # On vérifie si l'orientation du murs est valide ou s'il y a déjà un
        # murs à cette position, sinon on soulève une erreur
        if ((orientation == "vertical" and position in self.verticaux) or
                (orientation == "horizontal" and position in self.horizontaux)):
            raise QuoridorError

        # On vérifie la position des murs verticaux,
        # si invalide on soulève une erreur
        if orientation == 'vertical':
            if (not 2 <= position[0] <= 9 or
                    not 1 <= position[1] <= 8):
                raise QuoridorError
        # On vérifie la position des murs horizontaux,
        # si invalide on soulève une erreur
        if orientation == 'horizontal':
            if (not 1 <= position[0] <= 8 or
                    not 2 <= position[1] <= 9):
                raise QuoridorError

        # On vérifie si le joueur 1 et sélectionné et qu'il a
        # placé tous ses murs, on soulève une erreur
        if (joueur == 1 and not self.joueur1["murs"]):
            raise QuoridorError

        # On vérifie si le joueur 2 et sélectionné et dans qu'il a
        # placé tous ses murs, on soulève une erreur
        if (joueur == 2 and not self.joueur2["murs"]):
            raise QuoridorError

        # On place le position du murs dans sa liste correspondante si aucune
        # des erreurs possiblent n'a été soulevées
        if orientation == "vertical":
            self.verticaux.append(position)
        if orientation == "horizontal":
            self.horizontaux.append(position)

        # On incrémente le nombre de mur restant
        if joueur == 1:
            self.joueur1["murs"] += -1
        if joueur == 2:
            self.joueur2["murs"] += -1


class QuoridorError(Exception):
    """
    Gère les exceptions dans la class Quoridor
    """
    pass


def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """
    Crée le graphe des déplacements admissibles pour les joueurs.

    :param joueurs: une liste des positions (x,y) des joueurs.
    :param murs_horizontaux: une liste des positions (x,y) des murs horizontaux.
    :param murs_verticaux: une liste des positions (x,y) des murs verticaux.
    :returns: le graphe bidirectionnel (en networkX) des déplacements admissibles.
    """
    graphe = nx.DiGraph()

    # pour chaque colonne du damier
    for x in range(1, 10):
        # pour chaque ligne du damier
        for y in range(1, 10):
            # ajouter les arcs de tous les déplacements possibles pour cette tuile
            if x > 1:
                graphe.add_edge((x, y), (x-1, y))
            if x < 9:
                graphe.add_edge((x, y), (x+1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y-1))
            if y < 9:
                graphe.add_edge((x, y), (x, y+1))

    # retirer tous les arcs qui croisent les murs horizontaux
    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y-1), (x, y))
        graphe.remove_edge((x, y), (x, y-1))
        graphe.remove_edge((x+1, y-1), (x+1, y))
        graphe.remove_edge((x+1, y), (x+1, y-1))

    # retirer tous les arcs qui croisent les murs verticaux
    for x, y in murs_verticaux:
        graphe.remove_edge((x-1, y), (x, y))
        graphe.remove_edge((x, y), (x-1, y))
        graphe.remove_edge((x-1, y+1), (x, y+1))
        graphe.remove_edge((x, y+1), (x-1, y+1))

    # retirer tous les arcs qui pointent vers les positions des joueurs
    # et ajouter les sauts en ligne droite ou en diagonale, selon le cas
    for joueur in map(tuple, joueurs):

        for prédécesseur in list(graphe.predecessors(joueur)):
            graphe.remove_edge(prédécesseur, joueur)

            # si admissible, ajouter un lien sauteur
            successeur = (2*joueur[0]-prédécesseur[0], 2*joueur[1]-prédécesseur[1])

            if successeur in graphe.successors(joueur) and successeur not in joueurs:
                # ajouter un saut en ligne droite
                graphe.add_edge(prédécesseur, successeur)

            else:
                # ajouter les liens en diagonal
                for successeur in list(graphe.successors(joueur)):
                    if prédécesseur != successeur and successeur not in joueurs:
                        graphe.add_edge(prédécesseur, successeur)

    # ajouter les noeuds objectifs des deux joueurs
    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')

    return graphe
