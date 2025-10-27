
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

def serializer_round(obj):
    """Convertit un objet Python en JSON"""
    if isinstance(obj, Round): # Vérification que l'objet de classe crée "obj" est bien du même type que Tournament
        data_round = {"Matchs": obj.matchs, 
                        "Nom du tour":obj.name_round, 
                        "Date et heure du début du tour": obj.date_and_hour_of_start,
                        "Date et heure de fin du tour":obj.date_and_hour_of_end}
        return data_round
    raise TypeError(f"Type non sérialisable: {type(obj)}")

