import random
from views.view_match import display_score, display_players, display_player_add_to_match
from models.model_match import Match


#CREATION DE MATCH
def create_match(list_player):
    list_match_player = [] #Liste des joueurs jouant le match
    
    for _ in range(2):
        random_choice_player = random.randint(0, len(list_player)-1)
        if list_player[random_choice_player] not in list_match_player:
            list_match_player.append(list_player[random_choice_player])
            list_player.remove(list_player[random_choice_player])
        else:
            random_choice_player = random.randint(0, len(list_player)-1)
            list_match_player.append(list_player[random_choice_player])
            
    
    return Match(players=list_match_player, score=0)

#GESTION DE LA CREATION DE MATCH
def manage_winner_match(list_match_player):
    score = 0
    winner = random.randint(0, 1) 
    print("Le gagnant du match est:",list_match_player[winner])
    list_match_player[winner].score +=1
    return {list_match_player[winner]}



