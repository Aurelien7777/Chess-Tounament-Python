import json

class Tournament:
    def __init__(self, place, date_of_start, date_of_end, number_of_round, actual_round, match, list_of_round, list_player, description):
        self.place = place
        self.date_of_start = date_of_start
        self.date_of_end = date_of_end
        self.number_of_round = 4
        self.actual_round = actual_round
        self.match = match
        self.list_of_round = list_of_round
        self.list_player = list_player
        self.description = description
        
    def points_calculation(self):
        pass
    
class Player:
    def __init__(self, name, last_name, date_of_birth, id):
        self.name = name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.id = id
    
    def __repr__(self):
        return f"Player(nom={self.name},prenom={self.last_name} ,date de naissance={self.date_of_birth}, ID={self.id})"


class Match:
    #Un tuple contenant 2 listes contenant elles-mêmes un joueur et un score
    def __init__(self, players, score):
        self.players = players
        self.score  = score

class Round:
    def __init__(self, matchs, name_round):
        self.matchs = matchs
        self.name_round = name_round
        

class Serialisation:
    def __init__(self):
        pass
    