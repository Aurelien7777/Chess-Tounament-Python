

class Tournament:
    def __init__(self, name_of_tournament, place, date_of_start, date_of_end, actual_round, list_of_round, list_player_saved, description):
        self.name_of_tournament = name_of_tournament
        self.place = place
        self.date_of_start = date_of_start
        self.date_of_end = date_of_end
        self.number_of_round = 4 #Nombre de tours
        self.actual_round = actual_round
        self.list_of_round = list_of_round
        self.list_player_saved = list_player_saved
        self.description = description
        
    def points_calculation(self):
        pass
    
class Round:
    def __init__(self, matchs, name_round, date_of_start, date_of_end):
        self.matchs = matchs #Liste de matchs
        self.name_round = name_round
        self.date_of_start = date_of_start
        self.date_of_end = date_of_end
        
class Match:
    #Un tuple contenant 2 listes contenant elles-mêmes un joueur et un score
    def __init__(self, players, score):
        self.players = players # Paire de joueurs (liste ou tuple)
        self.score  = score #1 point victoire / 0 point défaite / 0.5 point match nul