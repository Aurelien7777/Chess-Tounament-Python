import random
import json
from views.view import display_name, display_menu, display_lastname, display_date_of_birth, display_id,display_created_player
from views.view import display_place, display_date_of_start, display_date_of_end, display_description, display_actual_round
from views.view import display_player_add_to_match
from models.model import Player,Tournament

#CREATION DE JOUEUR
def create_player():
    
    name = display_name()
    last_name = display_lastname()
    date_of_birth = display_date_of_birth()
    id = display_id()   
    player = Player(name=name,date_of_birth=date_of_birth,last_name=last_name,id=id)
    display_created_player(name, last_name)
    
    return player


#CREATION DE TOURNOI
def create_tournament():
    place = display_place()
    date_of_start = display_date_of_start()
    date_of_end = display_date_of_end()
    description = display_description()
    actual_round = display_actual_round()
    tournament = Tournament(place=place,date_of_start=date_of_start,date_of_end=date_of_end,
                            description=description, actual_round=actual_round, number_of_round=1, 
                            match="",list_of_round="", list_player="") 
    return tournament


#CREATION DE MATCH
def create_match(list_player):
    list_match_player = []
    
    for i in range(2):
        random_choice_player = random.randint(0, len(list_player))
        list_match_player.append(list_player[random_choice_player])
        for player in list_match_player:    
            display_player_add_to_match(list_player, random_choice_player)
    return list_match_player

def serializer(obj):
    """Convertit un objet Python en JSON"""
    if isinstance(obj, Player):
        data_player = {"name": obj.name, "date_of_birth": obj.date_of_birth, "last_name":obj.last_name, "id":obj.id}
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
    
    if choice == 1:
        player = create_player() #CREATION JOUEUR
        all_players.append(player)
        save_players(all_players) #CREATION D'UN FICHIER JSON
    elif choice == 2:
        if len(all_players) < 2:
            print("Pas assez de joueurs pour créer un match.")
        else:
            manage_create_match(all_players) #CREATION MATCH
    elif choice == 3: 
        manage_create_tournament()




#CREATION MATCH
def manage_create_match(all_players):
    # ex : tirer 2 joueurs différents
    p1, p2 = random.sample(all_players, 2)  # évite doublon & off-by-one
    create_match([p1, p2])
    

def save_players(players):
    # sérialiser une **liste** complète (pas concaténer deux JSON)
    data = []
    for p in players:
        data_player = serializer(p)
        data.append(data_player)
    
    with open('data_players.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        

#CREATION TOURNAMENT
def manage_create_tournament():
    create_tournament()








