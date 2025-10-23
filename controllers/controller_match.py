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
    # print("La liste des joueurs classé par point qui va être utilisé pour les matchs est:\n")
    compteur = 1
    for classement in classement_after_round:
        # print(f"No.{compteur}   {classement.name} {classement.last_name} score : {classement.score} ID : {classement.id}")
        compteur += 1
    print()

    # Pas assez de joueurs
    if len(classement_after_round) < 2:
        return None

    # On prend le meilleur disponible (index 0)
    p1 = classement_after_round[0]

    # On cherche le meilleur partenaire possible (index 1, puis 2, etc.)
    k = 1
    
    while k < len(classement_after_round):
        p2 = classement_after_round[k]
        match_key = {p1.id, p2.id}

        # Si la paire n'a jamais joué, on VALIDE et on enlève les deux
        if match_key not in matches_played:
            matches_played.append(match_key)
            # retirer p2 AVANT p1 (pour ne pas décaler l'index 0)
            classement_after_round.pop(k)
            classement_after_round.pop(0)
            return Match(players=[p1, p2], score=0)

        # Sinon, on tente le suivant
        k += 1

    # Si p1 n’a aucun partenaire disponible (tous déjà joués), on l’enlève et on retente
    classement_after_round.pop(0)
    return match_after_first_round(classement_after_round, matches_played)



    

#GESTION DES RESULTATS DES MATCHS 
def manage_winner_match_bis(list_match_player):
    
    winner = random.randint(0, 2)
    # print("Le chiffre choisi est:", winner)
    print()
    
    if winner == 0: #Si le chiffre choisi est inférieur à 1 soit est égal à 0 

        # print(f"le perdant est: {list_match_player[1]}\nle gagnant est {list_match_player[0]}")
        list_match_player[0].score += 1
        return list_match_player[winner], list_match_player[1]
    
    elif winner == 1:

        # print(f"le perdant est: {list_match_player[0]}\nle gagnant est {list_match_player[1]}")
        list_match_player[1].score += 1
        return list_match_player[winner], list_match_player[0]
    
    elif winner == 2 : #Si le chiffre choisi est supérieur à 1 = Match nul

        draw_list = []
        list_match_player[0].score +=0.5
        list_match_player[1].score +=0.5
        
        draw_list.append(list_match_player[0])
        draw_list.append(list_match_player[1])
        # print("Match nul") #Chaque joueur reçoit 0,5 point si le match se termine par un match nul.
        print(draw_list)
        return draw_list




#GESTION DU CLASSEMENT DES JOUEURS
def classement(winner_list, draw_list, looser_list):
    
    classement_after_match = []
    for winner in winner_list:
        classement_after_match.append(winner)
    print()
    for draw in draw_list:
        classement_after_match.append(draw)
    print()
    for looser in looser_list:
        classement_after_match.append(looser)
    print()

    #  initialisation score max et score min à partir du 1er joueur si la liste n'est pas vide
    if classement_after_match:
        score_max = classement_after_match[0].score
        score_min = classement_after_match[0].score
    else:
        score_max = 0
        score_min = 0

    itération = 0
    while itération < len(classement_after_match):
        player_classement = classement_after_match[itération]

        # mise à jour des score max et min 
        if player_classement.score >= score_max:
            score_max = player_classement.score
        elif player_classement.score <= score_min:
            score_min = player_classement.score

        # insertion triée (remontée du joueur si besoin)
        if itération > 0:
            joueur = itération
            while joueur > 0 and classement_after_match[joueur].score > classement_after_match[joueur-1].score:
                temporaire = classement_after_match[joueur-1]
                classement_after_match[joueur-1] = classement_after_match[joueur]
                classement_after_match[joueur] = temporaire
                joueur -= 1

        itération += 1

    # supprimer les doublons par id (on garde la 1re occurrence) 
    current_idx = 0
    while current_idx < len(classement_after_match):
        next_idx = current_idx + 1
        while next_idx < len(classement_after_match):
            if classement_after_match[next_idx].id == classement_after_match[current_idx].id:
                classement_after_match.pop(next_idx)
            else:
                next_idx += 1
        current_idx += 1

    print()
    compteur = 1
    for player_classement_final in classement_after_match:
        print(f"No.{compteur}   {player_classement_final.name} {player_classement_final.last_name} score : {player_classement_final.score} ID : {player_classement_final.id}")
        compteur += 1

    return classement_after_match



def choice_white_or_black(list_match_player):
    player_start = random.randint(0, 1)
    print(f"Le joueur jouant en blanc est {list_match_player[player_start].name } {list_match_player[player_start].last_name }")
    return player_start