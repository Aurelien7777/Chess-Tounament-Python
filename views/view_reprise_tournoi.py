def display_rebuild_round(rebuilding_rounds):
    """Indique à l'utilisateur la reprise d'un round incomplet."""

    print(f"\n Reprise du {rebuilding_rounds[-1].name_round} (incomplet)")


def display_initialisation_played_pairs():
    """Indique à l'utilisateur l'initialisation des paires déjà jouées."""

    print("\n Initialisation des paires déjà jouées dans ce round...")


def display_pause_tournament():
    """Indique à l'utilisateur la pause du tournoi."""

    print("Pause du tournoi")


def display_no_possible_match():
    """Indique à l'utilisateur qu'aucun match n'est possible dans ce round."""

    print("\n  Aucun match possible dans ce round")


def display_end_round(data_tournament, round_obj):
    """Indique à l'utilisateur la fin d'un round."""

    print(f"    Fin du {data_tournament.actual_round} à {round_obj.date_and_hour_of_end}")


def display_no_match_played_in_this_round():
    """Indique à l'utilisateur qu'aucun match n'a été joué dans ce round."""

    print("     Aucun match joué dans ce round. Pause du tournoi.")


def display_player_draws():
    """Indique à l'utilisateur qu'un match s'est terminé par un match nul."""

    print("   Résultat: Match nul (0.5 - 0.5)")


def display_player_wins(winner):
    print(f"   Résultat: {winner[0].name} {winner[0].last_name} gagne (1 - 0)")


def display_player_loses(winner):
    print(f"   Résultat: {winner[0].name} {winner[0].last_name} gagne (0 - 1)")


def display_tournament_finished(data_tournament):
    print(f"\n TOURNOI TERMINE ! ({data_tournament.number_of_round} rounds joués)")


def display_final_classement():
    print("\n CLASSEMENT FINAL:")


def display_player_final_ranking(idx, player):
    print(f"{idx}. {player.name} {player.last_name} - {player.score} points")


def display_end_of_round(data_tournament, round_obj):
    print(f"\n Fin du {data_tournament.actual_round} à {round_obj.date_and_hour_of_end}")


def display_classement_apres_round(data_tournament):
    print(f"\n CLASSEMENT APRES {data_tournament.actual_round} :")


def display_player_ranking_after_round(idx, player):
    print(f"{idx}. {player.name} {player.last_name} - {player.score} points")


def display_tournament_not_found():
    print("Tournoi introuvable.")


def display_number_of_match(number_of_match):
    print(f"\n Nombre de matchs par round: {number_of_match}")


def display_matches_played(round_match_list, number_of_match):
    print(f"   Matchs déjà joués : {len(round_match_list)}/{number_of_match}")


def display_remaining_matches(remaining_matches):
    print(f"   Matchs restants : {remaining_matches}")


def display_start_round(round_obj):
    print(f"\nDébut du {round_obj.name_round} à {round_obj.date_and_hour_of_start}")


def display_match_count(round_match_list, number_of_match):
    print(f"\n  Match {len(round_match_list)}/{number_of_match}:")


def display_match_information(match_after_round):
    print(f"   {match_after_round.players[0].name} {match_after_round.players[0].last_name} ")


def display_match_opponent(match_after_round):
    print(f"   contre {match_after_round.players[1].name} {match_after_round.players[1].last_name}")


def request_name_tournament_resume():
    return input("Nom du tournoi à reprendre: ").strip()


def request_continue_tournament():
    return input("Voulez-vous continuer le tournoi? (oui/non) :").strip().lower()
