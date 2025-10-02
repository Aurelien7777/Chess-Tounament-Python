import random
from .view_match import display_score, display_players, display_player_add_to_match


#CREATION DE MATCH
def create_match(list_player):
    list_match_player = [] #Liste des joueurs jouant le match
    
    for player in list_player:
        random_choice_player = random.randint(0, len(list_player)-1)
        if list_player[random_choice_player] not in list_match_player:
            list_match_player.append(list_player[random_choice_player])
            display_player_add_to_match(list_player, random_choice_player)
    return list_match_player

#GESTION DE LA CREATION DE MATCH
def manage_winner_match(list_match_player):
    # ex : tirer 2 joueurs différents
    winner = random.randint(0, 1)  # évite doublon & off-by-one
    print("Le gagnant du match est:",list_match_player[winner])
    

