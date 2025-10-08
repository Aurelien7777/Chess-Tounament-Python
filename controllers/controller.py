import random
import json
from views.view import display_name, display_menu, display_lastname, display_date_of_birth, display_created_player, ask_player_creation
from models.model import Player
from .controller_tournament import create_tournament
from models.model_tournament import Tournament
from .controller_match import manage_winner_match, create_match
from models.model import Player
from models.model_round import Round
from pathlib import Path
import os
from .controller_round import start_round
import datetime


#CREATION DE JOUEUR
def create_player():

    name = display_name()
    last_name = display_lastname()
    date_of_birth = display_date_of_birth() 
    id = ""
    player = Player(name=name,date_of_birth=date_of_birth,last_name=last_name,id=id, score=0)
    display_created_player(name, last_name)
    
    return player

#SAUVEGARDE DU JOUEUR DANS UN FICHIER JSON
def save_players(players): # "players" contient la liste des joueurs qui vont être sauvegardés
    # sérialiser une **liste** complète (pas concaténer deux JSON)
    data = []
    for player in players: #Itération sur la liste contenant les infos des joueurs
        print("Le joueur sauvegardé est:", player)
        data_player = serializer(player) #Récupération et conversion des infos joueurs au format JSON
        print("les données sauvegardées sont:", data_player)
        data.append(data_player) #Ajout des infos joueurs à la liste
    
    
    
    if not os.path.exists("data_players.json"):
        with open('data_players.json', 'w', encoding='utf-8') as f: #Création d'un fichier JSON 
            json.dump(data, f, ensure_ascii=False, indent=2) #Ecriture dans le fichier
    else: 
        with open('data_players.json', 'a', encoding='utf-8') as f: #Création d'un fichier JSON 
            json.dump(data, f, ensure_ascii=False, indent=2) #Ecriture dans le fichier



#CONVERTISSEMENT D'UN OBJET PYTHON EN JSON
def serializer(obj):
    """Convertit un objet Python en JSON"""
    if isinstance(obj, Player): #Vérification que l'objet de classe crée "obj" est bien du même type que Player
        data_player = {"name": obj.name, "last_name":obj.last_name, "date_of_birth": obj.date_of_birth, "id":obj.id, "score":obj.score}
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
            print("Le type du joueur crée est:", type(player))
            print()
            all_players.append(player)
            print("Le type du joueur présent dans la liste est:", type(all_players[0]))
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
        #play_match = Match()
        while len(all_players) <= 1:
            player = create_player()
            all_players.append(player)
        else:
            single_match = create_match(all_players) #CREATION MATCH
            winner_match = manage_winner_match(single_match)
            
    #TOURNAMENT
    elif choice == 3:
        #CREATION DU TOURNOI
        tournament = create_tournament() 
        number_player_in_tournamment = int(input("Combien de joueurs participe au tournoi? ")) #Nombre de joueurs participant au tournoi
        
        #CREATION DES JOUEURS DU TOURNOI 
        for player in range(number_player_in_tournamment):
            player = create_player()
            print()
            all_players.append(player) #Enregistrement des joueurs dans la liste des joueurs sauvegardés
        save_players(all_players) #Enregistrement des joueurs dans le fichier JSON
        print()
        
        tournament.list_player_saved = all_players #Utilisation de la variable de l'objet Tournament
        number_of_match = int(number_player_in_tournamment / 2) #Détermination du nombre de match
        
        round_match_list = [] #Création d'une liste contenant l'ensemble des matchs par round
        winner_list = [] #Création d'une liste contenant l'ensemble des gagnants des matchs
        short_lived_list = all_players.copy()
        #Réalisation des matchs pour le round 1 
        
        for tour in range(tournament.number_of_round): #Execution des 4 rounds
            Round.name_round = f"Round {tour+1}" #Nom du round
            Round.date_and_hour_of_start = datetime.datetime.now()
            tournament.actual_round = Round.name_round
            print(f"Début du {Round.name_round} à {Round.date_and_hour_of_start}")
            print()
            short_lived_list = all_players.copy()
            round_match_list = [] #Création d'une liste contenant l'ensemble des matchs par round
            
            for match in range(number_of_match):
                match = create_match(short_lived_list) #Sélection aléatoire de 2 joueurs dans la liste "all_players " qui contient tous les joueurs
                unique_match = ([match.players[0], match.score], [match.players[1], match.score])
                round_match_list.append(unique_match) #Ajout du match qui vient d'être crée juste au-dessus dans la liste de tous les matchs du round
                print()
                print("Le match est:", unique_match)
                winner = manage_winner_match(match.players) #Décide du vainqueur du match
                print()
                winner_list.append(winner) #Ajout du vainqueur dans une liste
                print()
                
            Round.date_and_hour_of_end = datetime.datetime.now()
            print(f"Fin du {tournament.actual_round} à {Round.date_and_hour_of_end}")
            #print("Voici les vainqueurs des différentes rencontres: ", winner_list)
            
            






