
def display_pause_tournament():
    print("Pause du tournoi")
    
#===================================
# GESTION DES MATCHS
#===================================
    
def display_start_round(round_obj):
    print(f"Début du {round_obj.name_round} à {round_obj.date_and_hour_of_start}\n")
    
def display_information_round(tournament):
    print(f"MATCHS DU {tournament.actual_round.upper()}\n")

def display_no_possible_match():
    print("Aucun match possible (plus assez de joueurs ou plus de paires disponibles).\n")
    
def display_match_information(match):
    print(f"Le match est {match.players[0].name} {match.players[0].last_name} contre {match.players[1].name} {match.players[1].last_name}\n")

def display_end_round(tournament, round_obj):
    print(f"Fin du {tournament.actual_round} à {round_obj.date_and_hour_of_end}\n")

def display_no_match_played_in_this_round():
    print("Aucun match joué dans ce round. Pause du tournoi.")
    


#===============================
# GESTION DES CLASSEMENTS
#===============================
def display_classement_apres_round_1():
    print("CLASSEMENT APRES ROUND 1\n")

def display_classement_apres_round(round_obj):
    print(f"CLASSEMENT APRES ROUND {round_obj.name_round}:\n")