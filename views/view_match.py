# ===================================
# GESTION DES MATCHS
# ===================================
def display_players():
    players = []
    print("Les joueurs participants au match sont ")
    return players


def display_score():
    score = 0
    print(score)
    return score


def display_player_add_to_match(list_player, random_choice_player):
    return print(f"Le joueur {list_player[random_choice_player]} a été ajouté au match")


# ===================================
# GESTION DES RESULTATS DES MATCHS
# ===================================


def choice_winner_match():
    print("Entrez le numéro du vainqueur du match [0, 1 ou 2].")
    return int(input("Le vainqueur du match est : "))


def display_input_result_of_match_invalid():
    print("Entrée invalide. Veuillez entrer 0, 1 ou 2.\n")


def display_classement_final(compteur, player_classement_final):
    print(
        f"No.{compteur}\n"
        f"    {player_classement_final.name}\n"
        f"    {player_classement_final.last_name}\n"
        f"    score : {player_classement_final.score}\n"
        f"    ID : {player_classement_final.id}"
    )


def display_white_player(list_match_player, player_start):
    print(
        f"""Le joueur jouant en blanc est:
    {list_match_player[player_start].name} {list_match_player[player_start].last_name}"""
    )
