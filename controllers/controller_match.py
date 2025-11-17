import random
from views.view_match import (
    display_input_result_of_match_invalid,
    display_classement_final,
    display_white_player,
    choice_winner_match,
)

from models.model_match import Match


# CREATION DE MATCH
def create_match(list_player, matches_played):
    """Crée un match entre deux joueurs aléatoires n'ayant pas encore joué ensemble."""

    list_match_player = []  # Liste des joueurs jouant un match

    if len(list_player) < 2:
        return None

    for _ in range(2):
        if len(list_player) == 0:
            break  # sécurité pour éviter "empty range in randrange"

        random_choice_player = random.randint(
            0, len(list_player) - 1
        )  # Choix d'un chiffre aléatoire
        chosen_player = list_player[random_choice_player]  # Joueur choisi

        if chosen_player not in list_match_player:
            list_match_player.append(chosen_player)
            list_player.remove(chosen_player)

    if len(list_match_player) == 2:
        # Crée un identifiant unique du match (ordre neutre)
        match_key = tuple(sorted((list_match_player[0].id, list_match_player[1].id)))

        if match_key in matches_played:
            return create_match(list_player, matches_played)
        else:
            matches_played.append(match_key)
            return Match(players=list_match_player, score=[0, 0])  # retour ajouté

    else:
        return None


def match_after_first_round(classement_after_round, matches_played_round):
    """
    Sélectionne deux joueurs du classement qui n'ont pas encore joué ensemble
    dans le round actuel. Ne modifie pas directement matches_played_round.
    """

    # Pas assez de joueurs pour créer un match
    if len(classement_after_round) < 2:
        return None

    # Parcourt tous les joueurs possibles pour trouver une paire valide
    for i in range(len(classement_after_round)):
        premier_du_classement = classement_after_round[i]
        for j in range(
            i + 1, len(classement_after_round)
        ):  # Je prends le joueur suivant dans le classement
            deuxieme_meilleur = classement_after_round[j]

            # Clé de la paire (ordre neutre)
            match_key = tuple(sorted((premier_du_classement.id, deuxieme_meilleur.id)))

            # Vérifie si la paire n'a jamais joué dans ce round
            if match_key not in matches_played_round:
                matches_played_round.append(match_key)
                classement_after_round.remove(premier_du_classement)
                classement_after_round.remove(deuxieme_meilleur)
                return Match(
                    players=[premier_du_classement, deuxieme_meilleur], score=[0, 0]
                )  # retour ajouté

    # Si aucune paire valide trouvée
    return None


# GESTION DES RESULTATS DES MATCHS
def manage_winner_match_bis(list_match_player):
    """Gère le résultat d'un match entre deux joueurs."""

    winner = -1
    while winner == -1 or winner > 2:
        try:
            winner = choice_winner_match()
        except ValueError:
            display_input_result_of_match_invalid()
            return manage_winner_match_bis(list_match_player)

    if winner == 0:  # Si le chiffre choisi est inférieur à 1 soit est égal à 0

        list_match_player[0].score += 1
        return list_match_player[winner], list_match_player[1]

    elif winner == 1:

        list_match_player[1].score += 1
        return list_match_player[winner], list_match_player[0]

    elif winner == 2:  # Si le chiffre choisi est supérieur à 1 = Match nul

        draw_list = []
        list_match_player[0].score += 0.5
        list_match_player[1].score += 0.5

        draw_list.append(list_match_player[0])
        draw_list.append(list_match_player[1])
        return draw_list


# GESTION DU CLASSEMENT DES JOUEURS
def classement(winner_list, draw_list, looser_list):
    """Gère le classement des joueurs après un round."""

    classement_after_match = []
    for winner in winner_list:
        classement_after_match.append(winner)

    for draw in draw_list:
        classement_after_match.append(draw)

    for looser in looser_list:
        classement_after_match.append(looser)

    #  initialisation score max et score min à partir du 1er joueur si la liste n'est pas vide
    if classement_after_match:
        score_max = classement_after_match[0].score
        score_min = classement_after_match[0].score
    else:
        score_max = 0
        score_min = 0

    itération = 0
    while itération < len(classement_after_match):  # parcours de la liste des joueurs
        player_classement = classement_after_match[
            itération
        ]  # Sélection du joueur courant

        # mise à jour des score max et min
        if player_classement.score >= score_max:
            score_max = player_classement.score
        elif player_classement.score <= score_min:
            score_min = player_classement.score

        # insertion triée (remontée du joueur si besoin)
        if itération > 0:
            joueur = itération
            while (
                joueur > 0
                and classement_after_match[joueur].score
                > classement_after_match[joueur - 1].score
            ):
                temporaire = classement_after_match[joueur - 1]
                classement_after_match[joueur - 1] = classement_after_match[joueur]
                classement_after_match[joueur] = temporaire
                joueur -= 1

        itération += 1

    # supprimer les doublons par id (on garde la 1re occurrence)
    current_idx = 0
    while current_idx < len(classement_after_match):
        next_idx = current_idx + 1
        while next_idx < len(classement_after_match):
            if (
                classement_after_match[next_idx].id
                == classement_after_match[current_idx].id
            ):
                classement_after_match.pop(next_idx)
            else:
                next_idx += 1
        current_idx += 1

    compteur = 1
    for player_classement_final in classement_after_match:
        display_classement_final(compteur, player_classement_final)
        compteur += 1

    return classement_after_match


def choice_white_or_black(list_match_player):
    """Choisit aléatoirement quel joueur joue avec les pièces blanches."""

    player_start = random.randint(0, 1)
    display_white_player(list_match_player, player_start)
    return list_match_player[player_start]


def serializer_match(obj):
    """Convertit un objet Python en JSON"""

    if isinstance(
        obj, Match
    ):  # Vérification que l'objet de classe crée "obj" est bien du même type que Tournament
        data_match = {"Matchs": obj.players, "Score": obj.score}
        return data_match
    raise TypeError(f"Type non sérialisable: {type(obj)}")
