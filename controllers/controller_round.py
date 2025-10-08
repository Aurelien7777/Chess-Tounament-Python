
from models.model_round import Round
from views.view_round import display_name_round, display_matchs, display_date_of_start, display_date_of_end
from tournaments.model_tournament import Tournament
import datetime

def start_round():
    name_round = display_name_round()
    date_and_hour_of_start = display_date_of_start()
    date_and_hour_of_end = display_date_of_end()
    matchs = display_matchs()
    
    
    
    round = Round(name_round=name_round,date_and_hour_of_start=date_and_hour_of_start, 
                date_and_hour_of_end=date_and_hour_of_end, matchs=matchs) 
    
    return round

