from controllers.controller_tournament import serializer_tournament

class Tournament:
    def __init__(self, name_of_tournament, place, date_of_start, date_of_end, actual_round, list_of_round, list_player_saved, description):
        self.name_of_tournament = name_of_tournament
        self.place = place
        self.date_of_start = date_of_start
        self.date_of_end = date_of_end
        self.number_of_round = 4 #Nombre de tours défini
        self.actual_round = actual_round #Liste de match
        self.list_of_round = list_of_round
        self.list_player_saved = list_player_saved
        self.description = description
        
    def points_calculation(self):
        pass
    