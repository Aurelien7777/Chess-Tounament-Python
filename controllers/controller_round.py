
from models.model_round import Round
from models.model_match import Match
from views.view_round import display_name_round, display_date_of_start, display_date_of_end, display_matchs
from models.model_tournament import Tournament

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
    """Reconstruit les rounds à partir des données JSON du tournoi et du dictionnaire des joueurs par ID."""
    
    rounds = [] # liste pour stocker les rounds reconstruits
    for round_tournoi in name_tournament["Informations des tours"]:
        # reconstruction du round avec le nom, la date de début et la date de fin
        r = Round(matchs=[], name_round=round_tournoi["Nom du round"],
                date_of_start=round_tournoi["Date de début"], date_of_end=round_tournoi["Date de fin"]) 
        
        for match_tournoi in round_tournoi["Matchs"]: # parcourir les matchs du round
            joueur_0_id = match_tournoi["Joueurs"][0]["id"] 
            joueur_1_id = match_tournoi["Joueurs"][1]["id"]
            
            joueur_0 = joueurs_par_id[joueur_0_id]
            joueur_1 = joueurs_par_id[joueur_1_id]
            
            # reconstruction du match avec les joueurs et le score
            match = Match(players=[joueur_0, joueur_1], score=match_tournoi["Score"]) 
            r.matchs.append(match) # ajouter le match reconstruit au round
        rounds.append(r) # ajouter le round reconstruit à la liste des rounds
    return rounds # retourner la liste des rounds reconstruits


def reconstruire_matches_played(rounds):
    """Reconstruit la liste des matchs déjà joués à partir des rounds."""
    
    match_deja_joue = []
    for round in rounds:
        for match in round.matchs:
            id_joueur1 = match.players[0].id
            id_joueur2 = match.players[1].id
            
            # normaliser l’ordre pour éviter les doublons inversés
            # si id_joueur1 < id_joueur2 alors pair = (id_joueur1, id_joueur2) sinon pair = (id_joueur2, id_joueur1)
            pair = (id_joueur1, id_joueur2) if id_joueur1 < id_joueur2 else (id_joueur2, id_joueur1) 
            if pair not in match_deja_joue:
                match_deja_joue.append(pair)
    return match_deja_joue # retourner la liste des paires de joueurs déjà joués
