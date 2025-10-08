import datetime

class Round:
    def __init__(self, matchs, name_round, date_of_start, date_of_end):
        self.matchs = matchs #Liste de matchs
        self.name_round = name_round
        self.date_and_hour_of_start = datetime.datetime.now()
        self.date_and_hour_of_end = datetime.datetime.now()
        
    def __repr__(self):
        return f"Round(matchs={self.matchs},nom du tour={self.name_round}, date et heure de début={self.date_and_hour_of_start}, date et heure de fin={self.date_and_hour_of_end}"