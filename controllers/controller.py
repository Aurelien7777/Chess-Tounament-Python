import random
import json
from views.view import display_name, display_menu, display_lastname, display_date_of_birth, display_created_player, ask_player_creation
from models.model import Player
from models.model_match import Match
from .controller_tournament import create_tournament, serializer_tournament
from models.model_tournament import Tournament
from .controller_match import create_match, match_after_first_round, manage_winner_match_bis, classement, choice_white_or_black
from models.model_round import Round
from pathlib import Path
import os
from .controller_round import start_round
import datetime
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage


# CREATION DE JOUEUR
def create_player():
    list_number_for_id = ["0","1","2","3","4","5","6","7","8","9"]
    list_letter_for_id = ["A","B","C","D","E","F","G","G","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    
    name = display_name()
    last_name = display_lastname()
    date_of_birth = display_date_of_birth() 
    list_for_id = random.sample(list_letter_for_id, k=2) + random.sample(list_number_for_id, k=5)
    id = "".join(list_for_id)
    player = Player(name=name,date_of_birth=date_of_birth,last_name=last_name,id=id, score=0)
    display_created_player(name, last_name)
    
    return player


def save_players(players, data_base_players): # "players" contient la liste des joueurs qui vont être sauvegardés
    # sérialiser une liste complète (pas concaténer deux JSON)
    data_base_players = TinyDB(
                        data_base_players,
                        storage=JSONStorage,
                        ensure_ascii=False, # garde les accents
                        indent=2,
                        encoding="utf-8") # indentations sur plusieurs lignes
    
    for player in players: # Itération sur la liste contenant les infos des joueurs
        if player not in data_base_players.all() and player not in data_base_players.all():
            data_player = serializer(player) # Récupération et conversion des infos joueurs au format JSON
            data_base_players.insert(data_player)
            print(f"Sauvegarde du joueur {player.name} {player.last_name} effectuée")
        else:
            print("Le joueur est déjà présent dans la base de donnée")
        
    return data_base_players


def save_score(data_base_players, players):
    db = TinyDB(
        data_base_players,
        storage=JSONStorage,
        ensure_ascii=False,
        indent=2,
        encoding="utf-8"
    )
    request_player = Query() # L'objet utilisé pour créer les requêtes

    for joueur in players:  # Parcours chaque joueur du tournoi
        data_player = serializer(joueur)  # récupère les données joueurs dont le score actuel (modifié dans manage_winner_match)
        
        # Recherche le joueur dans la base par id 
        request_id_player = (request_player.id == data_player["id"]) 
        existing = db.get(request_id_player)


        if existing:
            db.update({"score": data_player["score"]}, request_id_player) # Accès à la clé score du dictionnaire correspondant à l'ID du joueur concerné
            print(f"Score mis à jour pour {joueur.name} {joueur.last_name} : {joueur.score}")
        else:
            print(f"{joueur.name} {joueur.last_name} introuvable : pas de mise à jour")

    db.close()




def save_data(data_tournament, data_base_tournament):
    db = TinyDB(
        data_base_tournament,
        storage=JSONStorage,
        ensure_ascii=False,
        indent=2,
        encoding="utf-8"
    )
    
    data = serializer_tournament(data_tournament)
    db.insert(data)
    print(f"Sauvegarde du joueur des données du tournoi: {data}")
    
    return data_base_tournament


# CONVERTISSEMENT D'UN OBJET PYTHON EN JSON
def serializer(obj):
    """Convertit un objet Python en JSON"""
    if isinstance(obj, Player): # Vérification que l'objet de classe crée "obj" est bien du même type que Player
        data_player = {"name": obj.name, "last_name":obj.last_name, "date_of_birth": obj.date_of_birth, "id":obj.id, "score":obj.score}
        return data_player
    raise TypeError(f"Type non sérialisable: {type(obj)}")







#EXECUTION DU MENU PRINCIPAL
def start_menu():
    all_players = [] # Création d'une liste contenant les joueurs crées
    
    choice = int(display_menu()) # Récupération de la donnée entrée dans la fonction input de la fonction display_menu()
    if choice > 3 or choice < 1:
        print("ERREUR: Le choix doit être chiffre entre 1 et 3")
        try:
            choice = int(display_menu()) # Conversion en INT 
        except ValueError:
            print("ERREUR: Le choix doit être chiffre entre 1 et 3")


    # CHOIX UTILISATEUR
    
    # PLAYER
    if choice == 1:

        IsCreation = True
        while IsCreation:
            player = create_player() # CREATION JOUEUR
            print("Le type du joueur crée est:", type(player))
            print()
            all_players.append(player)
            print("Le type du joueur présent dans la liste est:", type(all_players[0]))
            save_players(all_players) # CREATION D'UN FICHIER JSON
            
            # Démarrage de la boucle pour création de joueur
            response = ask_player_creation()
            if response.lower() == "oui":
                try:
                    player = create_player() # CREATION JOUEUR
                    all_players.append(player)
                    save_players(all_players) # CREATION D'UN FICHIER JSON
                except TypeError:
                    print("ERREUR: La réponse ne peut être que Oui ou Non")
            else:
                IsCreation = False
                
            
        
    
    # MATCH
    elif choice == 2:
        while len(all_players) <= 1:
            player = create_player()
            all_players.append(player)
        else:
            single_match = create_match(all_players) # CREATION MATCH
            winner_match = manage_winner_match_bis(single_match)



    # TOURNAMENT
    elif choice == 3:
        # CREATION DU TOURNOI
        tournament = create_tournament() 
        data_base_tournament = save_data(tournament, "data_base_tournament.json") # Enregistrement des données du tournoi
        number_player_in_tournamment = int(input("Combien de joueurs participe au tournoi? ")) # Nombre de joueurs participant au tournoi
        
        # CREATION DES JOUEURS DU TOURNOI 
        for player in range(number_player_in_tournamment):
            player = create_player()
            print()
            all_players.append(player) # Enregistrement des joueurs dans la liste des joueurs sauvegardés
        
        tournament.list_player_saved = all_players.sort() # Utilisation de la variable de l'objet Tournament / liste des joueurs enregistrés
        data_base_players = save_players(tournament.list_player_saved, "data_base_players.json") # Enregistrement des joueurs dans le fichier JSON
        number_of_match = len(data_base_players) # Détermination du nombre de match en fonction du nombre de joueur divisé par 2
        round_match_list = [] # Création d'une liste contenant l'ensemble des matchs par round
        
        
        

        # REALISATION DES MATCHS POUR LE TOUR 1 
        for tour in range(1): #Execution du premier round 

            Round.name_round = f"Round {tour+1}" #Nom du round
            Round.date_and_hour_of_start = datetime.datetime.now()
            tournament.actual_round = Round.name_round
            print(f"Début du {Round.name_round} à {Round.date_and_hour_of_start}")
            print()
            short_lived_list = all_players.copy() # Copie de la liste pour la réutiliser dans la création des matchs
            round_match_list = [] # Création d'une liste contenant l'ensemble des matchs par round
            matches_played = [] #Liste des matchs joués par round
            

            winner_list = [] # Création d'une liste contenant l'ensemble des gagnants des matchs
            draw_list = [] # Création d'une liste contenant l'ensemble des joueurs ayant fait match nul
            looser_list = [] # Création d'une liste contenant l'ensemble des perdants des matchs
            

            # LANCEMENT DES MATCHS DU ROUND
            for match in range(number_of_match // 2):

                match = create_match(short_lived_list, matches_played) # Sélection aléatoire de 2 joueurs dans la copie de la liste "all_players " qui contient tous les joueurs
                if match is None:
                    print("Aucun match possible (plus assez de joueurs ou plus de paires disponibles).")
                    break
                unique_match = ([match.players[0], match.score], [match.players[1], match.score])
                choice_white_or_black(match.players)
                round_match_list.append(unique_match) # Ajout du match qui vient d'être crée juste au-dessus dans la liste de tous les matchs du round
                # print("Le match est:", unique_match)
                print(f"Le match est {match.players[0].name} {match.players[0].last_name} contre {match.players[1].name} {match.players[1].last_name}")
                print()


                # GESTION DES GAGNANT/PERDANT/MATCH NUL
                winner = manage_winner_match_bis(match.players) # Décide du vainqueur d'un match à travers la liste "match.players"
                
                if type(winner) == list:
                    draw_list.append(winner[0])
                    draw_list.append(winner[1])
                
                else:
                    winner_list.append(winner[0]) # Ajout du vainqueur dans une liste
                    looser_list.append(winner[1]) # Ajout du perdant dans la liste
                print()

                save_score("data_base_players.json", all_players)
                print()
            print()
            Round.date_and_hour_of_end = datetime.datetime.now()
            print(f"Fin du {tournament.actual_round} à {Round.date_and_hour_of_end}")
            print()
        tournament.list_of_round = round_match_list # liste des tours 
        print("CLASSEMENT APRES ROUND 1")
        classement_after_round = classement(winner_list, draw_list, looser_list) # Etablissement du classement après le premier round
        print()
        print()


        # REALISATION DES MATCHS POUR LES TOURS RESTANTS
        for tour in range(tournament.number_of_round - 1): #Execution du second round 

            Round.name_round = f"Round {tour+1}" #Nom du round
            Round.date_and_hour_of_start = datetime.datetime.now()
            tournament.actual_round = Round.name_round
            print(f"Début du {Round.name_round} à {Round.date_and_hour_of_start}")
            print()
            short_lived_list = all_players.copy() # Copie de la liste pour la réutiliser dans la création des matchs
            round_match_list = [] # Création d'une liste contenant l'ensemble des matchs par round
            matches_played = [] #Liste des matchs joués par round

            winner_list = [] # Création d'une liste contenant l'ensemble des gagnants des matchs
            draw_list = [] # Création d'une liste contenant l'ensemble des joueurs ayant fait match nul
            looser_list = [] # Création d'une liste contenant l'ensemble des perdants des matchs
            classement_after_round_bis = classement_after_round.copy()
            
            for match in range(number_of_match // 2):
                
                # MATCHS DES GAGNANTS
                print("MATCHS APRES LE PREMIER TOUR")
                match_after_round = match_after_first_round(classement_after_round_bis, matches_played) # Sélection aléatoire de 2 joueurs dans la copie de la liste "classement_after_round_bis" qui contient tous les joueurs
                if match_after_round is None:
                    print("Aucun match possible (plus assez de joueurs ou plus de paires disponibles).")
                else:
                    unique_match = ([match_after_round.players[0], match_after_round.score], [match_after_round.players[1], match_after_round.score])
                    choice_white_or_black(match_after_round.players)
                    round_match_list.append(unique_match) # Ajout du match qui vient d'être crée juste au-dessus dans la liste de tous les matchs du round
                    # print("Le match est:", unique_match)
                    
                # GESTION DES GAGNANT/PERDANT/MATCH NUL
                    winner = manage_winner_match_bis(match_after_round.players) # Décide du vainqueur d'un match à travers la liste "match.players"
                    if type(winner) == list:
                        draw_list.append(winner[0])
                        draw_list.append(winner[1])

                    else:
                        winner_list.append(winner[0]) # Ajout du vainqueur dans une liste
                        looser_list.append(winner[1]) # Ajout du perdant dans la liste
                print()


                save_score("data_base_players.json", all_players)
            print()
            Round.date_and_hour_of_end = datetime.datetime.now()
            print(f"Fin du {tournament.actual_round} à {Round.date_and_hour_of_end}")
            print()
        tournament.list_of_round = round_match_list # liste des tours 
        
        print(f"CLASSEMENT APRES ROUND {Round.name_round}:\n")
        classement_after_round = classement(winner_list, draw_list, looser_list) # Etablissement du classement après le premier round








