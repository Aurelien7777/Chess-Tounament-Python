#====================================
#CREATION DE JOUEUR
#====================================
def display_name() -> str:
    return input("Entrer le nom du joueur: ")

def display_lastname() -> str:
    return input("Entrer le prenom du joueur: ")

def display_date_of_birth() -> str:
    return input("Entrer la date de naissance du joueur: ")

def display_created_player(last_name, name):
    print(f"Création du joueur {last_name} {name} réussie")
    
def ask_player_creation():
    return input("Voulez-vous créer un nouveau joueur? Oui ou Non: ")


#====================================
#AFFICHAGE DU MENU
#====================================
def display_menu():
    print("Bienvenue dans le menu principal de l'outil de gestion des tournois d'échecs.\n")
    return  int(input("1 - Créer joueur \n2 - Créer match \n3 - Créer tournoi \n4 - Reprendre un tournoi \n5 - Générer un rapport \nEntrer votre choix: "))

def display_error_invalid_menu_choice():
    print("ERREUR: Le choix doit être chiffre entre 1 et 5")




#====================================
#AFFICHAGE DES MESSAGES DE CONFIRMATION ET D'ERREUR
#====================================
def display_save_player(player):
    print(f"\nSauvegarde du joueur {player.name} {player.last_name} effectuée")

def display_player_already_exists():
    print("Le joueur est déjà présent dans la base de donnée")
    
def display_updated_score(joueur):
    print(f"Score mis à jour pour {joueur.name} {joueur.last_name} : {joueur.score}")

def display_player_not_found(joueur):
    print(f"{joueur.name} {joueur.last_name} introuvable : pas de mise à jour")
    
    


def display_error_invalid_response():
    print("ERREUR: La réponse ne peut être que Oui ou Non")