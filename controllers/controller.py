import random
from views.view import display_name, display_menu, display_lastname, display_date_of_birth, display_created_player, ask_player_creation, display_save_player, display_player_already_exists, display_updated_score, display_player_not_found, display_error_invalid_response, display_error_invalid_menu_choice
from models.model import Player
from models.model_match import Match
from .controller_tournament import create_tournament, save_data, charger_tournoi_par_nom
from .controller_match import create_match, match_after_first_round, manage_winner_match_bis, classement, choice_white_or_black
from models.model_round import Round
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
    player = Player(name=name,
                    date_of_birth=date_of_birth,
                    last_name=last_name,
                    id=id, score=0)
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
            display_save_player(player)
        else:
            display_player_already_exists()
        
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
            display_updated_score(joueur)
        else:
            display_player_not_found(joueur)

    db.close()


# CONVERTISSEMENT D'UN OBJET PYTHON EN JSON
def serializer(obj):
    """Convertit un objet Python en JSON"""
    if isinstance(obj, Player): # Vérification que l'objet de classe crée "obj" est bien du même type que Player
        data_player = {"name": obj.name, "last_name":obj.last_name, "date_of_birth": obj.date_of_birth, "id":obj.id, "score":obj.score}
        return data_player
    raise TypeError(f"Type non sérialisable: {type(obj)}")


def charger_joueurs(data_base_players_path):
    data_base_player = TinyDB(data_base_players_path, storage=JSONStorage, ensure_ascii=False, indent=2, encoding="utf-8")
    
    joueurs = {}
    
    for info_player in data_base_player.all():
        
        joueur = Player(
            name=info_player["name"],
            last_name=info_player["last_name"],
            date_of_birth=info_player["date_of_birth"],
            id=info_player["id"],
            score=info_player["score"], # score cumulé
        )
        joueurs[joueur.id] = joueur
    data_base_player.close()
    return joueurs  # dict id -> Player


def joueurs_du_tournoi(file_tournament, joueurs_par_id):
    list_tournament_player = [] 
    # privilégier la liste officielle du tournoi
    if file_tournament.get("Liste des joueurs"): # 
        for player_in_tournament in file_tournament["Liste des joueurs"]:
            player_id_tournament = player_in_tournament["id"]
            player_from_data_base = joueurs_par_id.get(player_id_tournament)
            if player_from_data_base:
                list_tournament_player.append(player_from_data_base)
        return list_tournament_player
    
    # fallback : récupérer depuis les matchs joués
    for round_in_file_tournament in file_tournament["Informations des tours"]:
        for match_in_round in round_in_file_tournament["Matchs"]:
            for player_in_match in match_in_round["Joueurs"]:
                player_id = player_in_match["id"]
                player_data_base = joueurs_par_id.get(player_id)
                if player_data_base and player_data_base not in list_tournament_player:
                    list_tournament_player.append(player_data_base)
    return list_tournament_player


#====================================
# GESTION DES CHOIX UTILISATEUR 
#====================================

def handle_player_creation(all_players):
    IsCreation = True
    while IsCreation:
        # CREATION JOUEUR
        player = create_player()
        all_players.append(player)
        save_players(all_players) # CREATION D'UN FICHIER JSON
        
        # Démarrage de la boucle pour création de joueur
        response = ask_player_creation()
        if response.lower() == "oui":
            try:
                player = create_player() # CREATION JOUEUR
                all_players.append(player)
                save_players(all_players) # CREATION D'UN FICHIER JSON
            except TypeError:
                display_error_invalid_response()
        else:
            IsCreation = False
        
def handle_single_match_creation(all_players):
    while len(all_players) <= 1:
        player = create_player()
        all_players.append(player)
    else:
        single_match = create_match(all_players) # CREATION MATCH
        manage_winner_match_bis(single_match)
        
def handle_tournament_creation():
    from controllers.creation_tournoi import lancer_creation_tournoi
    lancer_creation_tournoi()
    

def handle_tournament_resume():
    from controllers.reprise_tournoi import resume_tournament
    resume_tournament()
    
def handle_report():
    pass


#=============================
#EXECUTION DU MENU PRINCIPAL
#=============================
def start_menu():
    all_players = [] # Création d'une liste contenant les joueurs crées
    
    choice = int(display_menu()) # Récupération de la donnée entrée dans la fonction input de la fonction display_menu()
    if choice > 5 or choice < 1:
        display_error_invalid_menu_choice()
        try:
            choice = int(display_menu()) # Conversion en INT 
        except ValueError:
            display_error_invalid_menu_choice()

    if choice == 1:
        handle_player_creation(all_players)

    elif choice == 2:
        handle_single_match_creation(all_players)

    elif choice == 3:
        # CREATION DU TOURNOI
        handle_tournament_creation()

    elif choice == 4:
        # Reprendre un tournoi existant 
        handle_tournament_resume()
        
    elif choice == 5:
        handle_report()