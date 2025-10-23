from views.view import display_name, display_menu, display_lastname, display_date_of_birth, display_created_player
from models.model import Player
from models.model_tournament import Tournament
from views.view_tournament import display_name_of_tournament, display_place, display_date_of_start, display_date_of_end, display_description, display_actual_round
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
    actual_round = ""
    tournament = Tournament(name_of_tournament=name_of_tournament,place=place,date_of_start=date_of_start,date_of_end=date_of_end,
                            description=description, actual_round=actual_round, list_of_round=[], list_player_saved=[]) 
    return tournament

def serializer_tournament(obj):
    """Convertit un objet Python en JSON"""
    if isinstance(obj, Tournament): # Vérification que l'objet de classe crée "obj" est bien du même type que Tournament
        data_tournament = {"Nom du tournoi": obj.name_of_tournament, 
                        "Lieu du tournoi":obj.place, 
                        "Date de début du tournoi": obj.date_of_start,
                        "Date de fin du tournoi":obj.date_of_end,
                        "Nombre de round":obj.number_of_round,
                        "Informations des tours":obj.list_of_round,
                        "Liste des joueurs":obj.list_player_saved,
                        "Description":obj.description}
        return data_tournament
    raise TypeError(f"Type non sérialisable: {type(obj)}")



#CREATION DU DOSSIER DATA/TOURNAMENT
def data_tournament_folder_creation():
    os.makedirs("DATA_TOURNAMENT", exist_ok=True)
    print("Création du dossier DATA TOURNAMENT effectué")
    with open(f"DATA_tournament/tournament""w", encoding="utf-8", newline="") as file:
        pass



