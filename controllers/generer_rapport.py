from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage


def generate_player_tournament_report(data_base_tournament_path="data_base_tournament.json"):
    """Génère un rapport des joueurs d'un tournoi spécifique triés par nom."""
    
    name_tournament_resume = input("Nom du tournoi choisi: ").strip()
    if not name_tournament_resume:
        print("Le nom du tournoi ne peut pas être vide.")
        return
    
    db = TinyDB(data_base_tournament_path, storage=JSONStorage, ensure_ascii=False, indent=2, encoding="utf-8") 
    object_request_tournoi = Query()
    
    # db.get va rechercher un tournoi possédant le même nom que celui entré par l'utilisateur
    request_tournoi = db.get(object_request_tournoi["Nom du tournoi"] == name_tournament_resume) 
    
    if request_tournoi is None:
        print(f"Aucun tournoi trouvé avec le nom '{name_tournament_resume}'.")
        db.close()
        return
    
    print("\nVoici la réponse obtenu:")

    liste_joueurs_triee = sorted(request_tournoi["Liste des joueurs"], key=lambda name_player: name_player['name'])
    for joueur in liste_joueurs_triee:
        print(f"Joueur trié: {joueur['name']} {joueur['last_name']}, ID: {joueur['id']}, Score: {joueur['score']}\n")
    
    db.close()





def generate_all_player_report(data_base_players_path="data_base_players.json"):
    """Génère un rapport de tous les joueurs disponibles dans la base de données."""
    
    db = TinyDB(data_base_players_path, storage=JSONStorage, ensure_ascii=False, indent=2, encoding="utf-8") 
    all_players = db.all()
    print(f"Le type de all_players est: {type(all_players)}")
    
    if not all_players:
        print("Aucun joueur trouvé dans la base de données.")
        db.close()
        return
    
    print("\nListe des joueurs disponibles:")
    liste_all_players_triee = sorted(all_players, key=lambda name_player: name_player['name'])
    for joueur in liste_all_players_triee:
        print(f"- {joueur['name']} {joueur['last_name']}, ID: {joueur['id']}, Score: {joueur['score']}")
    
    db.close()




def generate_tournament_report(data_base_tournament_path="data_base_tournament.json"):
    """Génère un rapport de tous les tournois disponibles dans la base de données."""
    
    db = TinyDB(data_base_tournament_path, storage=JSONStorage, ensure_ascii=False, indent=2, encoding="utf-8") 
    all_tournaments = db.all()
    
    if not all_tournaments:
        print("Aucun tournoi trouvé dans la base de données.")
        db.close()
        return
    
    print("\nListe des tournois disponibles:")
    for tournoi in all_tournaments:
        print(f"- {tournoi['Nom du tournoi']}")
    
    db.close()





def generate_name_and_date_tournament_report(data_base_tournament_path="data_base_tournament.json"):
    """Génère un rapport des noms et dates d'un tournoi'donné."""
    
    name_tournament = input("Nom du tournoi choisi: ").strip()
    if not name_tournament:
        print("Le nom du tournoi ne peut pas être vide.")
        return
    
    db = TinyDB(data_base_tournament_path, storage=JSONStorage, ensure_ascii=False, indent=2, encoding="utf-8") 
    object_request_tournoi = Query()
    
    # db.get va rechercher un tournoi possédant le même nom que celui entré par l'utilisateur
    request_tournoi = db.get(object_request_tournoi["Nom du tournoi"] == name_tournament) 
    
    if request_tournoi is None:
        print(f"Aucun tournoi trouvé avec le nom '{name_tournament}'.")
        db.close()
        return
    
    print("\nListe d'un tournoi avec nom et date:")
    print(f"- {request_tournoi['Nom du tournoi']}, Date de début: {request_tournoi['Date de début du tournoi']}, Date de fin: {request_tournoi['Date de fin du tournoi']}")
    
    db.close()




def generate_report_all_rounds_and_all_matches_of_tournament(data_base_tournament_path="data_base_tournament.json"):
    """Génère un rapport de tous les rounds et matchs d'un tournoi donné."""
    name_tournament = input("Nom du tournoi choisi: ").strip()
    if not name_tournament:
        print("Le nom du tournoi ne peut pas être vide.")
        return
    
    db = TinyDB(data_base_tournament_path, storage=JSONStorage, ensure_ascii=False, indent=2, encoding="utf-8") 
    object_request_tournoi = Query()
    
    # db.get va rechercher un tournoi possédant le même nom que celui entré par l'utilisateur
    request_tournoi = db.get(object_request_tournoi["Nom du tournoi"] == name_tournament) 
    
    if request_tournoi is None:
        print(f"Aucun tournoi trouvé avec le nom '{name_tournament}'.")
        db.close()
        return

    print(f"\nRapport des rounds et matchs pour le tournoi '{name_tournament}':")
    for round_info in request_tournoi["Informations des tours"]:
        print(f"\nRound: {round_info['Nom du round']}")
        print("  Matchs:")
        for match in round_info["Matchs"]:
            player1 = match["Joueurs"][0]
            player2 = match["Joueurs"][1]
            score = match["Score"]
            print(f"    - {player1['name']} {player1['last_name']} vs {player2['name']} {player2['last_name']} | Score: {score}")






if __name__ == "__main__":
    #generate_player_tournament_report()
    #generate_tournament_report()
    #generate_all_player_report()
    #generate_name_and_date_tournament_report()
    generate_report_all_rounds_and_all_matches_of_tournament()