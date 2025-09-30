#CREATION DE JOUEUR
def display_name() -> str:
    name = input("Entrer le nom du joueur: ")
    return name

def display_lastname() -> str:
    prenom = input("Entrer le prenom du joueur: ")
    return prenom

def display_date_of_birth() -> str:
    date_of_birth = input("Entrer la date de naissance du joueur: ")
    return date_of_birth

def display_id() -> str:
    id = input("Entrer le ID du joueur: ")
    return id

def display_created_player(last_name, name):
    print(f"Création du joueur {last_name} {name} réussie")


#CREATION MATCH
def display_players():
    players = []
    print("Les joueurs participants au match sont ")
    return players

def display_score():
    score = 0
    print(score)
    return score

def display_player_add_to_match(list_player, random_choice_player):
    print(f"Le joueur {list_player[random_choice_player]} a été ajouté au match")

#AFFICHAGE DU MENU
def display_menu():
    print("Bienvenue dans le menu principal de l'outil de gestion des tournois d'échecs.\n")
    menu_choice = int(input(f"1 - Créer joueur \n2 - Créer match \n3 - Créer tournoi \nEntrer votre choix: "))
    return menu_choice