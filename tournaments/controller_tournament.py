from views.view import display_name, display_menu, display_lastname, display_date_of_birth, display_created_player
from models.model import Player
from .model_tournament import Tournament
from .view_tournament import display_name_of_tournament, display_place, display_date_of_start, display_date_of_end, display_description, display_actual_round
from pathlib import Path
import os
import random


#CREATION DE TOURNOI
def create_tournament():
    name_of_tournament = display_name_of_tournament()
    place = display_place()
    date_of_start = display_date_of_start()
    date_of_end = display_date_of_end()
    description = display_description()
    actual_round = display_actual_round()
    tournament = Tournament(name_of_tournament=name_of_tournament,place=place,date_of_start=date_of_start,date_of_end=date_of_end,
                            description=description, actual_round=actual_round, list_of_round=[], list_player_saved=[]) 
    return tournament

def score_player_after_match():
    pass



#CREATION DU DOSSIER DATA/TOURNAMENT
def data_tournament_folder_creation():
    os.makedirs("DATA_TOURNAMENT", exist_ok=True)
    print("Création du dossier DATA TOURNAMENT effectué")
    with open(f"DATA_tournament/tournament""w", encoding="utf-8", newline="") as file:
        pass



