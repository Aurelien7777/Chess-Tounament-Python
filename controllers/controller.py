import random
import json
from views.view import display_name, display_menu, display_lastname, display_date_of_birth, display_created_player, ask_player_creation
from models.model import Player
from tournaments.controller_tournament import create_tournament
from matchs.controller_match import manage_winner_match, create_match
from pathlib import Path
import os
from tours.controller_round import start_round


#CREATION DE JOUEUR
def create_player():

    name = display_name()
    last_name = display_lastname()
    date_of_birth = display_date_of_birth() 
    id = ""
    player = Player(name=name,date_of_birth=date_of_birth,last_name=last_name,id=id)
    display_created_player(name, last_name)
    
    return player

#SAUVEGARDE DU JOUEUR DANS UN FICHIER JSON
def save_players(players):
    # sérialiser une **liste** complète (pas concaténer deux JSON)
    data = []
    for player in players: #Itération sur la liste contenant les infos des joueurs
        print("Le joueur sauvegardé est:", player)
        data_player = serializer(player) #Récupération et conversion des infos joueurs au format JSON
        print("les données sauvegardées sont:", data_player)
        data.append(data_player) #Ajout des infos joueurs à la liste
    
    with open('data_players.json', 'w', encoding='utf-8') as f: #Création d'un fichier JSON 
        json.dump(data, f, ensure_ascii=False, indent=2) #Ecriture dans le fichier

def add_player_in_jsonfile():
    pass


#CONVERTISSEMENT D'UN OBJET PYTHON EN JSON
def serializer(obj):
    """Convertit un objet Python en JSON"""
    if isinstance(obj, Player): #Vérification que l'objet de classe crée "obj" est bien du même type que Player
        data_player = {"name": obj.name, "last_name":obj.last_name, "date_of_birth": obj.date_of_birth, "id":obj.id}
        print(f"Les données du joueur sont {data_player}")
        return data_player
    raise TypeError(f"Type non sérialisable: {type(obj)}")







#EXECUTION DU MENU PRINCIPAL
def start_menu():
    all_players = [] #Création d'une liste contenant les joueurs crées
    
    choice = int(display_menu()) #Récupération de la donnée entrée dans la fonction input de la fonction display_menu()
    if choice > 3 or choice < 1:
        print("ERREUR: Le choix doit être chiffre entre 1 et 3")
        try:
            choice = int(display_menu()) #Conversion en INT 
        except ValueError:
            print("ERREUR: Le choix doit être chiffre entre 1 et 3")


    #CHOIX UTILISATEUR
    
    #PLAYER
    if choice == 1:

        IsCreation = True
        while IsCreation:
            player = create_player() #CREATION JOUEUR
            all_players.append(player)

            if not os.path.exists("data_players.json"):
                save_players(all_players) #CREATION D'UN FICHIER JSON
            
            #Démarrage de la boucle pour création de joueur
            response = ask_player_creation()
            if response.lower() == "oui":
                try:
                    player = create_player() #CREATION JOUEUR
                    all_players.append(player)
                    save_players(all_players) #CREATION D'UN FICHIER JSON
                except TypeError:
                    print("ERREUR: La réponse ne peut être que Oui ou Non")
            else:
                IsCreation = False
                
            
        
    
    #MATCH
    elif choice == 2:
        
        while len(all_players) <= 1:
            player = create_player()
            all_players.append(player)
        else:
            create_match(all_players) #CREATION MATCH
            manage_winner_match(all_players)
            
    #TOURNAMENT
    elif choice == 3:
        create_tournament()
        number_player_in_tournamment = input("Combien de joueurs participe au tournoi? ")
        
        for player in range(number_player_in_tournamment):
            player = create_player()
            all_players.append(player)
            
            number_of_match = number_player_in_tournamment / 2
            for match in number_of_match:
                match = create_match()
                
        start_round()






