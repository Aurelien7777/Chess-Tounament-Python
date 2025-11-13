
#===============================
# Vues pour les tournois
#===============================

def display_name_of_tournament():
    return input("Entrer le nom du tournoi: ")

def display_place():
    return input("Entrer le lieu du tournoi: ")

def display_date_of_start():
    return input("Entrer la date de début du tournoi: ")

def display_date_of_end():
    return input("Entrer la date de fin du tournoi: ")

def display_description():
    return input("Ajouter la description du tournoi: ")

def display_number_of_round():
    pass

def display_actual_round():
    actual_round = 0
    print(f"Nous sommes actuellement au tour {actual_round}")
    return actual_round



#===============================
# Vue pour la sauvegarde du tournoi
#===============================
def display_save_tournament(data):
    print(f"Sauvegarde des données du tournoi: {data['Nom du tournoi']}\n")
    
def display_update_tournament():
    print("Mise à jour des données du tournoi effectuée\n")