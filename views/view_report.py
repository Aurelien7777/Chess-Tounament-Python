
def display_ask_tournament_name():
    """Indique à l'utilisateur de saisir le nom du tournoi"""
    
    print("Le nom du tournoi ne peut pas être vide.")
    

def display_get_tournament_name():
    """Demande à l'utilisateur de saisir le nom du tournoi."""
    
    return input("Nom du tournoi choisi: ").strip()

def display_if_tournament_not_found(name_tournament_resume):
    """Indique à l'utilisateur que le tournoi n'a pas été trouvé dans la base de données."""
    
    if name_tournament_resume:
        (f"Aucun tournoi trouvé avec le nom '{name_tournament_resume}'.")
    else:
        print("Aucun tournoi trouvé dans la base de données.")
        
    
def display_sorted_players(joueur):
    """Affiche les informations d'un joueur trié."""
    
    print(f"Joueur trié: {joueur['name']} {joueur['last_name']}, ID: {joueur['id']}, Score: {joueur['score']}\n")
    
    
def display_no_players_found():
    """Indique à l'utilisateur qu'aucun joueur n'a été trouvé dans la base de données."""
    
    print("Aucun joueur trouvé dans la base de données.")
    
def display_introduction_available_players():
    """Affiche l'introduction pour l'affichage liste des joueurs disponibles."""
    
    print("\nListe des joueurs disponibles:")
    
def display_introduction_available_tournaments():
    """Affiche l'introduction pour l'affichage liste des tournois disponibles."""
    
    print("\nListe des tournois disponibles:")
    
def display_all_tournaments(tournoi):
    """Affiche les tournois trouvés."""
    
    print(f"- {tournoi['Nom du tournoi']}")
    
def display_introduction_tournament_with_date(tournoi):
    """Affiche l'introduction pour l'affichage liste des tournois avec nom et date."""
    
    print("\nListe d'un tournoi avec nom et date:")
    
def display_tournament_with_name_and_date(request_tournoi):
    """Affiche le nom et les dates d'un tournoi donné."""
    
    print(f"- {request_tournoi['Nom du tournoi']}, Date de début: {request_tournoi['Date de début du tournoi']}, Date de fin: {request_tournoi['Date de fin du tournoi']}")
    
def display_introduction_report_rounds_and_matches(name_tournament):
    """Affiche l'introduction pour l'affichage des rounds et matchs d'un tournoi donné."""
    
    print(f"\nRapport des rounds et matchs pour le tournoi '{name_tournament}':")
    
def display_rounds_and_matches(round_info):
    """Préparation de l'affichage des rounds et matchs d'un tournoi donné."""
    
    print(f"\nRound: {round_info['Nom du round']}")
    print("  Matchs:")
    
def display_match_info(player1, player2, score):
    """Affiche les informations d'un match."""
    print(f"    - {player1['name']} {player1['last_name']} vs {player2['name']} {player2['last_name']} | Score: {score}")
    
    
def display_menu_report_choice():
    print("Choisir le rapport à obtenir.\n")
    return  int(input("1 - Tous les joueurs par ordre alphabétique \n2 - Tous les tournois \n3 - Nom et dates d’un tournoi donné \n4 - Liste des joueurs du tournoi par ordre alphabétique \n5 - Liste de tous les tours du tournoi et de tous les matchs du tour. \nEntrer votre choix: "))
    
def display_error_invalid_menu_choice():
    print("ERREUR: Le choix doit être chiffre entre 1 et 5")
    