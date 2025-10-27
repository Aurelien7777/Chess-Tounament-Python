from views.view import display_name, display_menu, display_lastname, display_date_of_birth, display_created_player
from models.model import Player
from models.model_tournament import Tournament
from views.view_tournament import display_name_of_tournament, display_place, display_date_of_start, display_date_of_end, display_description, display_actual_round
from pathlib import Path
import os
import random
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage

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

        def player_to_dict(player):
            return {
                "name": player.name,
                "last_name": player.last_name,
                "date_of_birth": player.date_of_birth,
                "id": player.id,
                "score": player.score,
            }
            
            
        def match_to_dict(match):
            return {
                "Joueurs": [player_to_dict(p) for p in match.players],
                "Score": match.score,
            }
                
        def round_to_dict(round_obj):
            return {
                "Nom du round": round_obj.name_round,
                "Date de début": str(round_obj.date_and_hour_of_start),
                "Date de fin": str(round_obj.date_and_hour_of_end),
                "Matchs": [match_to_dict(m) for m in round_obj.matchs],
            }
        
        
        data_tournament = {"Nom du tournoi": obj.name_of_tournament, 
                        "Lieu du tournoi":obj.place, 
                        "Date de début du tournoi": obj.date_of_start,
                        "Date de fin du tournoi":obj.date_of_end,
                        "Nombre de round":obj.number_of_round,
                        "Informations des tours":[round_to_dict(r) for r in obj.list_of_round],
                        "Liste des joueurs": [player_to_dict(p) for p in obj.list_player_saved],
                        "Description":obj.description}
        return data_tournament
    raise TypeError(f"Type non sérialisable: {type(obj)}")

def save_data(data_tournament, data_base_tournament):
    
    db = TinyDB(
        data_base_tournament,
        storage=JSONStorage,
        ensure_ascii=False,
        indent=2,
        encoding="utf-8"
    )
    
    # Conversion des données en dictionnaire
    data = serializer_tournament(data_tournament)
    
    request_tournament = Query() # L'objet utilisé pour créer les requêtes
    
    request_data_tournament = (request_tournament["Nom du tournoi"] == data["Nom du tournoi"])
    
    existing = db.get(request_data_tournament)
    if not existing:
        # Insertion des données dans le fichier Json
        db.insert(data)
        print(f"Sauvegarde des données du tournoi: {data['Nom du tournoi']}")
        
    else:
        # db.update({"Liste des joueurs": data["Liste des joueurs"]}, request_data_tournament)
        db.update({"Informations des tours": data["Informations des tours"]}, request_data_tournament)
        db.update({"Description": data["Description"]}, request_data_tournament)
        db.update({"Lieu du tournoi": data["Lieu du tournoi"]}, request_data_tournament)
        db.update({"Date de début du tournoi": data["Date de début du tournoi"]}, request_data_tournament)
        db.update({"Date de fin du tournoi": data["Date de fin du tournoi"]}, request_data_tournament)
        db.update({"Nombre de round": data["Nombre de round"]}, request_data_tournament)
        print("Mise à jour des données du tournoi effectuée")
        
    db.close()
    return data_base_tournament




#CREATION DU DOSSIER DATA/TOURNAMENT
def data_tournament_folder_creation():
    os.makedirs("DATA_TOURNAMENT", exist_ok=True)
    print("Création du dossier DATA TOURNAMENT effectué")
    



