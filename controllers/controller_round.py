
from models.model_round import Round
from models.model_match import Match
from views.view_round import display_name_round, display_matchs, display_date_of_start, display_date_of_end
from models.model_tournament import Tournament
import datetime

def start_round():
    name_round = display_name_round()
    date_and_hour_of_start = display_date_of_start()
    date_and_hour_of_end = display_date_of_end()
    matchs = display_matchs()
    
    round = Round(name_round=name_round,date_and_hour_of_start=date_and_hour_of_start, 
                date_and_hour_of_end=date_and_hour_of_end, matchs=matchs) 
    
    return round

def serializer_round(obj):
    """Convertit un objet Python en JSON"""
    if isinstance(obj, Round): # Vérification que l'objet de classe crée "obj" est bien du même type que Tournament
        data_round = {"Matchs": obj.matchs, 
                        "Nom du tour":obj.name_round, 
                        "Date et heure du début du tour": obj.date_and_hour_of_start,
                        "Date et heure de fin du tour":obj.date_and_hour_of_end}
        return data_round
    raise TypeError(f"Type non sérialisable: {type(obj)}")


def reconstruire_rounds(name_tournament, joueurs_par_id):
    rounds = []
    for round_tournoi in name_tournament["Informations des tours"]:
        r = Round(matchs=[], name_round=round_tournoi["Nom du round"],
                date_of_start=round_tournoi["Date de début"], date_of_end=round_tournoi["Date de fin"])
        
        for match_tournoi in round_tournoi["Matchs"]:
            joueur_0_id = match_tournoi["Joueurs"][0]["id"]
            joueur_1_id = match_tournoi["Joueurs"][1]["id"]
            
            joueur_0 = joueurs_par_id[joueur_0_id]
            joueur_1 = joueurs_par_id[joueur_1_id]
            match = Match(players=[joueur_0, joueur_1], score=match_tournoi["Score"])  # Score = [1,0] etc.
            r.matchs.append(match)
        rounds.append(r)
    return rounds


def reconstruire_matches_played(rounds):
    match_deja_joue = []
    for round in rounds:
        for match in round.matchs:
            id_joueur1 = match.players[0].id
            id_joueur2 = match.players[1].id
            
            # normaliser l’ordre pour éviter les doublons inversés
            pair = (id_joueur1, id_joueur2) if id_joueur1 < id_joueur2 else (id_joueur2, id_joueur1)
            if pair not in match_deja_joue:
                match_deja_joue.append(pair)
    return match_deja_joue
