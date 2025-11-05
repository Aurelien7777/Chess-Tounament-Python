import random
import json
from views.view import display_name, display_menu, display_lastname, display_date_of_birth, display_created_player, ask_player_creation
from models.model import Player
from models.model_match import Match
from .controller_tournament import create_tournament, save_data, charger_tournoi_par_nom
from models.model_tournament import Tournament
from .controller_match import create_match, match_after_first_round, manage_winner_match_bis, classement, choice_white_or_black, serializer_match
from models.model_round import Round
from .controller_round import serializer_round, reconstruire_rounds, reconstruire_matches_played
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


def joueurs_du_tournoi(doc_tournoi, joueurs_par_id):
    lst = []
    # 1) privilégier la liste officielle du tournoi
    if doc_tournoi.get("Liste des joueurs"):
        for j in doc_tournoi["Liste des joueurs"]:
            pid = j["id"]
            p = joueurs_par_id.get(pid)
            if p:
                lst.append(p)
        return lst
    # 2) fallback : récupérer depuis les matchs joués
    for r_doc in doc_tournoi["Informations des tours"]:
        for m_doc in r_doc["Matchs"]:
            for j_doc in m_doc["Joueurs"]:
                pid = j_doc["id"]
                p = joueurs_par_id.get(pid)
                if p and p not in lst:
                    lst.append(p)
    return lst


#EXECUTION DU MENU PRINCIPAL
def start_menu():
    all_players = [] # Création d'une liste contenant les joueurs crées
    
    choice = int(display_menu()) # Récupération de la donnée entrée dans la fonction input de la fonction display_menu()
    if choice > 4 or choice < 1:
        print("ERREUR: Le choix doit être chiffre entre 1 et 4")
        try:
            choice = int(display_menu()) # Conversion en INT 
        except ValueError:
            print("ERREUR: Le choix doit être chiffre entre 1 et 4")


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
        tournament = create_tournament() # CREATION D'UN OBJET "TOURNAMENT"
        data_base_tournament = save_data(tournament, "data_base_tournament.json") # Enregistrement des données du tournoi
        number_player_in_tournamment = int(input("Combien de joueurs participe au tournoi? ")) # Nombre de joueurs participant au tournoi
        
        # CREATION DES JOUEURS DU TOURNOI 
        for _ in range(number_player_in_tournamment):
            player = create_player()
            print()
            all_players.append(player) # Enregistrement des joueurs dans la liste des joueurs sauvegardés
        
        tournament.list_player_saved = all_players # Utilisation de la variable de l'objet Tournament / liste des joueurs enregistrés
        data_base_players = save_players(tournament.list_player_saved, "data_base_players.json") # Enregistrement des joueurs dans le fichier JSON
        
        number_of_match = len(data_base_players) # Détermination du nombre de match en fonction du nombre de joueur divisé par 2
        round_match_list = [] # Création d'une liste contenant l'ensemble des matchs par round
        save_data(tournament, "data_base_tournament.json")
        
        # A CET ENDROIT AJOUTER LA POSSIBLITE DE COUPER/ FAIRE PAUSE / IF LE TOUR 1 A DEJA ETE JOUER ON REPREND AU SUIVANT
        # POUVOIR LE FAIRE AVANT/APRES UN MATCH
        continuer_tournoi = True 
        # REALISATION DES MATCHS POUR LE TOUR 1 
        for tour in range(1): #Execution du premier round 
            
            round_obj = Round(matchs=[], name_round=f"Round {tour+1}",
                date_of_start=datetime.datetime.now(),
                date_of_end=None)
            
            tournament.actual_round = round_obj.name_round
            print(f"Début du {round_obj.name_round} à {round_obj.date_and_hour_of_start}")
            print()
            short_lived_list = all_players.copy() # Copie de la liste pour la réutiliser dans la création des matchs
            round_match_list = [] # Création d'une liste contenant l'ensemble des matchs par round
            matches_played = [] #Liste des matchs joués par round
            

            winner_list = [] # Création d'une liste contenant l'ensemble des gagnants des matchs
            draw_list = [] # Création d'une liste contenant l'ensemble des joueurs ayant fait match nul
            looser_list = [] # Création d'une liste contenant l'ensemble des perdants des matchs
            

            # LANCEMENT DES MATCHS DU ROUND
            for _ in range(number_of_match // 2):
                
                if not continuer_tournoi:
                    break
                
                ask_for_continue = input("Voulez-vous continuer le tournoi? (oui/non) :").strip().lower()
                if ask_for_continue != "oui":
                    print("Pause du tournoi")
                    continuer_tournoi = False
                    break
                    
                match = create_match(short_lived_list, matches_played) # Sélection aléatoire de 2 joueurs dans la copie de la liste "all_players " qui contient tous les joueurs
                if match is None:
                    print("Aucun match possible (plus assez de joueurs ou plus de paires disponibles).")
                    break
                
                choice_white_or_black(match.players) # choix des couleurs 
                round_match_list.append(match) # Ajout du match qui vient d'être crée juste au-dessus dans la liste de tous les matchs du round
                
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
                    
                # score du match pris en compte dans le fichier JSON
                s1, s2 = 0, 0
                if type(winner) == list:
                    s1 = s2 = 0.5
                elif winner[0] is match.players[0]:
                    s1, s2 = 1, 0
                else:
                    s1, s2 = 0, 1

                match.score = [s1, s2]   # enregistre le résultat du match
                
                save_data(tournament, "data_base_tournament.json")
                save_score("data_base_players.json", all_players)
                
                print()

            # clôture du round 1
            if round_match_list:
                round_obj.matchs = round_match_list 
                round_obj.date_and_hour_of_end = datetime.datetime.now()
                tournament.list_of_round.append(round_obj)
                save_data(tournament, "data_base_tournament.json")
                
                print(f"Fin du {tournament.actual_round} à {round_obj.date_and_hour_of_end}")
            else:
                print("Aucun match joué dans ce round. Pause du tournoi.")
                return
            
            if not continuer_tournoi:
                return
            print()
            

        print("CLASSEMENT APRES ROUND 1")
        classement_after_round = classement(winner_list, draw_list, looser_list) # Etablissement du classement après le premier round
        print()
        save_data(tournament, "data_base_tournament.json")
        print()



        
        # REALISATION DES MATCHS POUR LES TOURS RESTANTS
        for tour in range(tournament.number_of_round - 1): #Execution du second round 
            
            round_obj = Round(matchs=[], name_round=f"Round {tour+2}",
                    date_of_start=datetime.datetime.now(),
                    date_of_end=None)

            
            tournament.actual_round = round_obj.name_round
            print(f"Début du {round_obj.name_round} à {round_obj.date_and_hour_of_start}")
            print()
            short_lived_list = all_players.copy() # Copie de la liste pour la réutiliser dans la création des matchs
            round_match_list = [] # Création d'une liste contenant l'ensemble des matchs par round
            matches_played_round = [] #Liste des matchs joués par round

            winner_list = [] # Création d'une liste contenant l'ensemble des gagnants des matchs
            draw_list = [] # Création d'une liste contenant l'ensemble des joueurs ayant fait match nul
            looser_list = [] # Création d'une liste contenant l'ensemble des perdants des matchs
            classement_after_round_bis = classement_after_round.copy()
            
            for _ in range(number_of_match // 2):
                
                if not continuer_tournoi:
                    break
                                
                ask_for_continue = input("Voulez-vous continuer le tournoi? (oui/non) :").strip().lower()
                if ask_for_continue != "oui":
                    print("Pause du tournoi")
                    continuer_tournoi = False
                    break
                
                # MATCHS DES GAGNANTS
                print("MATCHS APRES LE PREMIER TOUR")
                # Sélection aléatoire de 2 joueurs dans la copie de la liste "classement_after_round_bis" qui contient tous les joueurs
                match_after_round = match_after_first_round(classement_after_round_bis, matches_played_round) 
                if match_after_round is None:
                    print("Aucun match possible (plus assez de joueurs ou plus de paires disponibles).")
                else:
                    choice_white_or_black(match_after_round.players)
                    round_match_list.append(match_after_round) # Ajout du match qui vient d'être crée juste au-dessus dans la liste de tous les matchs du round


                # GESTION DES GAGNANT/PERDANT/MATCH NUL
                    winner = manage_winner_match_bis(match_after_round.players) # Décide du vainqueur d'un match à travers la liste "match.players"
                    if type(winner) == list:
                        draw_list.append(winner[0])
                        draw_list.append(winner[1])

                    else:
                        winner_list.append(winner[0]) # Ajout du vainqueur dans une liste
                        looser_list.append(winner[1]) # Ajout du perdant dans la liste
                        
                    # score du match pris en compte dans le fichier JSON
                    s1, s2 = 0, 0
                    if type(winner) == list:
                        s1 = s2 = 0.5
                    elif winner[0] is match_after_round.players[0]:
                        s1, s2 = 1, 0
                    else:
                        s1, s2 = 0, 1

                    match_after_round.score = [s1, s2]   # enregistre le résultat du match
                    save_score("data_base_players.json", all_players)
                    save_data(tournament, "data_base_tournament.json")
                    print()
                    
            if round_match_list:
                save_data(tournament, "data_base_tournament.json")
                round_obj.matchs = round_match_list 
                round_obj.date_and_hour_of_end = datetime.datetime.now()
                tournament.list_of_round.append(round_obj)
                print(f"Fin du {tournament.actual_round} à {round_obj.date_and_hour_of_end}")
            else:
                print("Aucun match joué dans ce round. Pause du tournoi.")
                return
                
            # si pause, on sort du choix 3 proprement
            if not continuer_tournoi:
                return
            print()

        
        print(f"CLASSEMENT APRES ROUND {round_obj.name_round}:\n")
        classement_after_round = classement(winner_list, draw_list, looser_list) # Etablissement du classement après le premier round
        save_data(tournament, "data_base_tournament.json")


    elif choice == 4:
        # Reprendre un tournoi existant 
        nom_tournoi = input("Nom du tournoi à reprendre: ").strip()
        charge = charger_tournoi_par_nom("data_base_tournament.json", nom_tournoi)
        if not charge:
            print("Tournoi introuvable.")
            return
        tournoi, objet_name_tournament = charge

        # Charger tous les joueurs (depuis la base joueurs)
        joueurs_par_id = charger_joueurs("data_base_players.json")

        # Reconstruire les rounds + paires déjà jouées
        rounds = reconstruire_rounds(objet_name_tournament, joueurs_par_id)
        
        # Lister les joueurs de CE tournoi (objets Player)
        all_players = joueurs_du_tournoi(objet_name_tournament, joueurs_par_id)

        # Réinjecter l'état dans l'objet tournoi
        tournoi.list_of_round = rounds
        number_of_match = len(all_players) // 2

        # Déterminer si on reprend un round incomplet ou si on démarre un nouveau round
        while True:
            if rounds and len(rounds[-1].matchs) < number_of_match:
                print(f"\nReprise du {rounds[-1].name_round} (incomplet)")
                round_obj = rounds[-1]
                tournoi.actual_round = round_obj.name_round
                current_round_index = len(rounds) - 1
                round_match_list = round_obj.matchs.copy()

                remaining_matches = number_of_match - len(round_match_list)
                print(f"   Matchs déjà joués : {len(round_match_list)}/{number_of_match}")
                print(f"   Matchs restants : {remaining_matches}")

                matches_played_this_round = []
                for match_round in round_match_list:
                    match_key = tuple(sorted((match_round.players[0].id, match_round.players[1].id)))
                    matches_played_this_round.append(match_key)

                classement_after_round = sorted(all_players, key=lambda p: p.score, reverse=True)

            else:
                current_round_index = len(rounds)
                if current_round_index >= tournoi.number_of_round:
                    print(f"\nTous les rounds du tournoi ont été joués ({tournoi.number_of_round} rounds)")
                    print("\nCLASSEMENT FINAL:")
                    classement_final = sorted(all_players, key=lambda p: p.score, reverse=True)
                    for idx, player in enumerate(classement_final, 1):
                        print(f"{idx}. {player.name} {player.last_name} - {player.score} points")
                    save_data(tournoi, "data_base_tournament.json")
                    return

                round_obj = Round(
                    matchs=[],
                    name_round=f"Round {current_round_index + 1}",
                    date_of_start=datetime.datetime.now(),
                    date_of_end=None
                )
                tournoi.actual_round = round_obj.name_round
                print(f"\nDébut du {round_obj.name_round} à {round_obj.date_and_hour_of_start}")

                round_match_list = []
                remaining_matches = number_of_match
                matches_played_this_round = []
                classement_after_round = sorted(all_players, key=lambda p: p.score, reverse=True)

            # Lancer les matchs restants du round
            for match_num in range(remaining_matches):
                ask_for_continue = input("\nVoulez-vous continuer le tournoi? (oui/non) : ").strip().lower()
                if ask_for_continue != "oui":
                    print("  Pause du tournoi")
                    if round_match_list:
                        round_obj.matchs = round_match_list
                        if round_obj not in tournoi.list_of_round:
                            tournoi.list_of_round.append(round_obj)
                    save_data(tournoi, "data_base_tournament.json")
                    return

                # joueurs déjà utilisés dans CE round
                joueurs_deja_joues = []
                for mk in matches_played_this_round:
                    joueurs_deja_joues.append(mk[0])
                    joueurs_deja_joues.append(mk[1])

                # joueurs disponibles
                classement_disponible = []
                for p in classement_after_round:
                    if p.id not in joueurs_deja_joues:
                        classement_disponible.append(p)
                if len(classement_disponible) < 2:
                    classement_disponible = classement_after_round[:]

                # chercher une paire non jouée dans CE round
                match_after_round = None
                i = 0
                while i < len(classement_disponible):
                    j = i + 1
                    while j < len(classement_disponible):
                        p1 = classement_disponible[i]
                        p2 = classement_disponible[j]
                        key = tuple(sorted((p1.id, p2.id)))
                        if key not in matches_played_this_round:
                            match_after_round = Match(players=[p1, p2], score=[0, 0])
                            matches_played_this_round.append(key)
                            break
                        j += 1
                    if match_after_round is not None:
                        break
                    i += 1

                if match_after_round is None:
                    print("\n  Aucun match possible dans ce round")
                    if round_match_list:
                        round_obj.matchs = round_match_list
                        round_obj.date_and_hour_of_end = datetime.datetime.now()
                        if round_obj not in tournoi.list_of_round:
                            tournoi.list_of_round.append(round_obj)
                        print(f"    Fin du {tournoi.actual_round} à {round_obj.date_and_hour_of_end}")
                    else:
                        print("     Aucun match joué dans ce round. Pause du tournoi.")
                    save_data(tournoi, "data_base_tournament.json")
                    return

                choice_white_or_black(match_after_round.players)
                round_match_list.append(match_after_round)

                print(f"\n  Match {len(round_match_list)}/{number_of_match}:")
                print(f"   {match_after_round.players[0].name} {match_after_round.players[0].last_name} "
                    f"contre {match_after_round.players[1].name} {match_after_round.players[1].last_name}")

                winner = manage_winner_match_bis(match_after_round.players)
                s1, s2 = 0, 0
                if isinstance(winner, list):
                    s1 = s2 = 0.5
                    print(f"   Résultat: Match nul (0.5 - 0.5)")
                elif winner[0] is match_after_round.players[0]:
                    s1, s2 = 1, 0
                    print(f"   Résultat: {winner[0].name} {winner[0].last_name} gagne (1 - 0)")
                else:
                    s1, s2 = 0, 1
                    print(f"   Résultat: {winner[0].name} {winner[0].last_name} gagne (0 - 1)")
                match_after_round.score = [s1, s2]

                save_score("data_base_players.json", all_players)
                classement_after_round = sorted(all_players, key=lambda p: p.score, reverse=True)

            # Clôture du round courant
            if round_match_list:
                round_obj.matchs = round_match_list
                round_obj.date_and_hour_of_end = datetime.datetime.now()
                if round_obj not in tournoi.list_of_round:
                    tournoi.list_of_round.append(round_obj)
                print(f"\n Fin du {tournoi.actual_round} à {round_obj.date_and_hour_of_end}")

                print(f"\n CLASSEMENT APRÈS {tournoi.actual_round}:")
                classement_apres = sorted(all_players, key=lambda p: p.score, reverse=True)
                for idx, player in enumerate(classement_apres, 1):
                    print(f"{idx}. {player.name} {player.last_name} - {player.score} points")

            save_data(tournoi, "data_base_tournament.json")

            # Si tournoi terminé → on sort
            if len(tournoi.list_of_round) >= tournoi.number_of_round:
                print(f"\n TOURNOI TERMINÉ ! ({tournoi.number_of_round} rounds joués)")
                print("\n CLASSEMENT FINAL:")
                classement_final = sorted(all_players, key=lambda p: p.score, reverse=True)
                for idx, player in enumerate(classement_final, 1):
                    print(f"{idx}. {player.name} {player.last_name} - {player.score} points")
                return

            # Sinon, proposer d'enchaîner sur le round suivant
            rep = input("\nDémarrer le round suivant ? (oui/non) : ").strip().lower()
            if rep != "oui":
                return

            # préparer la prochaine itération
            rounds = tournoi.list_of_round

        
            save_data(tournoi, "data_base_tournament.json")
            
            # Vérifier si le tournoi est terminé
            if len(tournoi.list_of_round) >= tournoi.number_of_round:
                print(f"\n TOURNOI TERMINÉ ! ({tournoi.number_of_round} rounds joués)")
                print("\n CLASSEMENT FINAL:")
                classement_final = sorted(all_players, key=lambda p: p.score, reverse=True)
                for idx, player in enumerate(classement_final, 1):
                    print(f'{idx}. {player.name} {player.last_name} - {player.score} points"){player.score} points')



