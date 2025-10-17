import random
from views.view_match import display_score, display_players, display_player_add_to_match
from models.model_match import Match
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage


#CREATION DE MATCH
def create_match(list_player, matches_played):
    
    list_match_player = [] #Liste des joueurs jouant un match
    
    if len(list_player) < 2:
        return None
    
    for _ in range(2):
        if len(list_player) == 0:
            break  # sécurité pour éviter "empty range in randrange"
    

        random_choice_player = random.randint(0, len(list_player)-1) # Choix d'un chiffre aléatoire
        chosen_player = list_player[random_choice_player] # Joueur choisi
        
        if chosen_player not in list_match_player:
            list_match_player.append(chosen_player)
            list_player.remove(chosen_player)
            
    if len(list_match_player) == 2:
        # Crée un identifiant unique du match (ordre neutre)
        match_key = {list_match_player[0].id, list_match_player[1].id}

        # Si ce match a déjà été joué = on en génère un autre
        if match_key in matches_played:
            return create_match(list_player, matches_played)
        else:
            matches_played.append(match_key)
            return Match(players=list_match_player, score=0)
    else:
        return None


def match_after_first_round(classement_after_round, matches_played):
    
    print("La liste des joueurs classé par point est:\n", classement_after_round)
    list_match_player = [] #Liste des joueurs jouant un match
    print("Nombre d'élément dans la liste classement:",len(classement_after_round))
    print()
    if len(classement_after_round) < 2:
        return None
    
    for i in range(2):
        if len(classement_after_round) < 2:
            print("Fin des matchs")
            break  # sécurité pour éviter "empty range in randrange"
        print("Nombre d'élément dans la liste classement:",len(classement_after_round))
        print()
        chosen_player = classement_after_round[i] # Joueur choisi
        
        if chosen_player not in list_match_player:
            list_match_player.append(chosen_player)
            classement_after_round.remove(chosen_player)
            
    if len(list_match_player) == 2:
        # Crée un identifiant unique du match (ordre neutre)
        match_key = {list_match_player[0].id, list_match_player[1].id}

        # Si ce match a déjà été joué = on en génère un autre
        if match_key in matches_played:
            return create_match(classement_after_round, matches_played)
        else:
            matches_played.append(match_key)
            return Match(players=list_match_player, score=0)
    else:
        return None
    
def classement(winner_list, draw_list, looser_list):
    
    classement_after_match = []
    for winner in winner_list:
        classement_after_match.append(winner)
        
    for draw in draw_list:
        classement_after_match.append(draw)

    for looser in looser_list:
        classement_after_match.append(looser)

    for classement in classement_after_match:
        print(classement)
        
    return classement_after_match
    


def manage_winner_match_bis(list_match_player):
    
    winner = random.randint(0, 2)
    print("Le chiffre choisi est:", winner)
    print()
    
    if winner == 0: #Si le chiffre choisi est inférieur à 1 soit est égal à 0 

        print(f"le perdant est: {list_match_player[1]}\nle gagnant est {list_match_player[0]}")
        list_match_player[0].score += 1
        return list_match_player[winner], list_match_player[1]
    
    elif winner == 1:

        print(f"le perdant est: {list_match_player[0]}\nle gagnant est {list_match_player[1]}")
        list_match_player[1].score += 1
        return list_match_player[winner], list_match_player[0]
    
    elif winner == 2 : #Si le chiffre choisi est supérieur à 1 = Match nul

        draw_list = []
        list_match_player[0].score +=0.5
        list_match_player[1].score +=0.5
        
        draw_list.append(list_match_player[0])
        draw_list.append(list_match_player[0])
        print("Match nul") #Chaque joueur reçoit 0,5 point si le match se termine par un match nul.
        print(draw_list)
        return draw_list














#GESTION DE LA CREATION DE MATCH
def manage_winner_match(list_match_player):
    
    winner = random.randint(0, 2)
    print("Le chiffre choisi est:", winner)
    print()
    
        
    if winner == 0: #Si le chiffre choisi est inférieur à 1 soit est égal à 0 
        print(f"le perdant est: {list_match_player[1]}\n le gagnant est {list_match_player[0]}")
        list_match_player[0].score += 1
        return list_match_player[winner]#, list_match_player[1]
    
    elif winner == 1:
        print(f"le perdant est: {list_match_player[0]}\n le gagnant est {list_match_player[1]}")
        list_match_player[1].score += 1
        return list_match_player[winner]#, list_match_player[0]
    
    elif winner == 2 : #Si le chiffre choisi est supérieur à 1 = Match nul
        list_match_player[0].score +=0.5
        list_match_player[1].score +=0.5
        print("Match nul") #Chaque joueur reçoit 0,5 point si le match se termine par un match nul.

        return list_match_player[0]#, list_match_player[1]
