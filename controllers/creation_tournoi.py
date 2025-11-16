import datetime
from .controller_tournament import create_tournament, save_data
from .controller_match import (
    create_match,
    match_after_first_round,
    manage_winner_match_bis,
    classement,
    choice_white_or_black,
)
from .controller import create_player, save_players, save_score
from models.model_round import Round
from views.view_creation_tournoi import (
    display_pause_tournament,
    display_start_round,
    display_information_round,
    display_no_possible_match,
    display_match_information,
    display_end_round,
    display_no_match_played_in_this_round,
    display_classement_apres_round_1,
    display_classement_apres_round,
    request_continue_tournament,
    request_number_of_players,
    display_finish_tournament,
)


def lancer_creation_tournoi():
    ALL_PLAYERS = []  # Création d'une liste contenant les joueurs crées

    # ================================
    # FONCTIONS DE CREATION DU TOURNOI
    # ================================

    # CREATION D'UN OBJET "TOURNAMENT"
    def creation_objet_tournoi():
        return create_tournament()

    # CREATION DES JOUEURS DU TOURNOI
    def creation_joueurs_tournoi(tournament, number_player_in_tournamment):
        for _ in range(number_player_in_tournamment):
            player = create_player()
            ALL_PLAYERS.append(player)  # Enregistrement des joueurs dans la liste des joueurs sauvegardés

        tournament.list_player_saved = (
            ALL_PLAYERS  # Utilisation de la variable de l'objet Tournament / liste des joueurs enregistrés
        )
        save_data(tournament, "data_base_tournament.json")  # Enregistrement des données du tournoi
        return save_players(
            tournament.list_player_saved, "data_base_players.json"
        )  # Enregistrement des joueurs dans le fichier JSON

    # CREATION DE L'OBJET ROUND
    def creation_objet_round(tour):
        # Création de l'objet Round
        return Round(
            matchs=[],
            name_round=f"Round {tour+1}",
            date_of_start=datetime.datetime.now(),
            date_of_end=None,
        )

    def pause_tournoi():
        ask_for_continue = request_continue_tournament()
        if ask_for_continue != "oui":
            display_pause_tournament()
            return False

    def gestion_gagnant_perdant(match, tournament, winner_list, draw_list, looser_list):
        """Gestion des gagnants, perdants et matchs nuls"""

        # Décide du vainqueur d'un match à travers la liste "match.players"
        winner = manage_winner_match_bis(match.players)

        if isinstance(winner, list):
            draw_list.append(winner[0])
            draw_list.append(winner[1])
        else:
            winner_list.append(winner[0])  # Ajout du vainqueur dans une liste
            looser_list.append(winner[1])  # Ajout du perdant dans la liste

        # score du match pris en compte dans le fichier JSON
        score_1, score_2 = 0, 0
        if isinstance(winner, list):
            score_1 = score_2 = 0.5
        elif winner[0] is match.players[0]:
            score_1, score_2 = 1, 0
        else:
            score_1, score_2 = 0, 1
        match.score = [score_1, score_2]  # enregistre le résultat du match

        save_data(tournament, "data_base_tournament.json")
        save_score("data_base_players.json", ALL_PLAYERS)

        return winner_list, draw_list, looser_list

    # ================================
    # CREATION DU TOURNOI
    # ================================
    tournament = creation_objet_tournoi()  # Création de l'objet Tournament
    save_data(tournament, "data_base_tournament.json")  # Enregistrement des données du tournoi

    number_player_in_tournamment = -1
    while number_player_in_tournamment % 2 != 0 or number_player_in_tournamment < 2:
        try:
            number_player_in_tournamment = request_number_of_players()  # Nombre de joueurs participant au tournoi
            if number_player_in_tournamment % 2 != 0 or number_player_in_tournamment < 2:
                raise ValueError("Le nombre de joueurs doit être un nombre pair et supérieur ou égal à 2.")
        except (ValueError, TypeError):
            print("Erreur : Veuillez entrer un nombre pair valide supérieur ou égal à 2.")

    # CREATION DES JOUEURS DU TOURNOI
    creation_joueurs_tournoi(tournament, number_player_in_tournamment)

    # Détermination du nombre de match en fonction du nombre de joueur divisé par 2
    number_of_match = len(ALL_PLAYERS)

    # Création d'une liste contenant l'ensemble des matchs par round
    round_match_list = []

    # Enregistrement des données du tournoi
    save_data(tournament, "data_base_tournament.json")

    # ================================
    # INITIALISATION DU TOURNOI - PREMIER ROUND
    # ================================
    for tour in range(1):
        # Création de l'objet Round
        round_obj = creation_objet_round(tour)

        # Mise à jour du round actuel dans l'objet Tournament
        tournament.actual_round = round_obj.name_round
        display_start_round(round_obj)

        # Enregistrement des données du tournoi
        save_data(tournament, "data_base_tournament.json")

        # Création d'une copie de la liste des joueurs pour la création des matchs
        short_lived_list = ALL_PLAYERS.copy()

        # Création d'une liste contenant l'ensemble des matchs par round
        round_match_list = []

        # Liste des matchs joués par round
        matches_played = []

        # Création d'une liste contenant l'ensemble des gagnants des matchs
        winner_list = []
        # Création d'une liste contenant l'ensemble des joueurs ayant fait match nul
        draw_list = []
        # Création d'une liste contenant l'ensemble des perdants des matchs
        looser_list = []

        # ================================
        # LANCEMENT DES MATCHS DU PREMIER ROUND
        # ================================
        for _ in range(number_of_match // 2):
            if pause_tournoi() is False:
                round_obj.matchs = round_match_list
                tournament.list_of_round.append(round_obj)
                save_data(tournament, "data_base_tournament.json")
                return

            display_information_round(tournament)

            # Sélection aléatoire de 2 joueurs dans la copie de la liste qui contient tous les joueurs
            match = create_match(short_lived_list, matches_played)
            if match is None:
                display_no_possible_match()
                break

            # Enregistrement des données du tournoi
            save_data(tournament, "data_base_tournament.json")

            # choix des couleurs
            choice_white_or_black(match.players)
            # Ajout du match qui vient d'être crée juste au-dessus dans la liste de tous les matchs du round
            round_match_list.append(match)
            # Affichage des joueurs du match
            display_match_information(match)

            # Enregistrement des données du tournoi
            save_data(tournament, "data_base_tournament.json")

            # GESTION DES GAGNANT/PERDANT/MATCH NUL
            resultat = gestion_gagnant_perdant(match, tournament, winner_list, draw_list, looser_list)
            # winner, draw, looser = gestion_gagnant_perdant(match, tournament, winner_list, draw_list, looser_list)
            # Enregistrement des données du tournoi
            save_data(tournament, "data_base_tournament.json")

        # clôture du round 1
        if round_match_list:
            round_obj.matchs = round_match_list
            round_obj.date_and_hour_of_end = datetime.datetime.now()
            tournament.list_of_round.append(round_obj)
            save_data(tournament, "data_base_tournament.json")
            display_end_round(tournament, round_obj)
        else:
            display_no_match_played_in_this_round()
            return

    # Etablissement du classement après le premier round
    display_classement_apres_round_1()

    classement_after_round = classement(resultat[0], resultat[1], resultat[2])
    # Enregistrement des données du tournoi
    save_data(tournament, "data_base_tournament.json")

    # ================================
    # REALISATION DES MATCHS POUR LES TOURS RESTANTS
    # ================================
    print(f"Nombre de rounds restants: {tournament.number_of_round - 1}\n")
    for tour in range(tournament.number_of_round - 1):  # Execution du second round

        # Création de l'objet Round + Ajout de 1 à l'indicateur "tour"
        round_obj = creation_objet_round(tour + 1)
        tournament.actual_round = round_obj.name_round
        display_start_round(round_obj)

        short_lived_list = ALL_PLAYERS.copy()  # Copie de la liste pour la réutiliser dans la création des matchs
        round_match_list = []  # Création d'une liste contenant l'ensemble des matchs par round
        matches_played_round = []  # Liste des matchs joués par round
        winner_list = []  # Création d'une liste contenant l'ensemble des gagnants des matchs
        draw_list = []  # Création d'une liste contenant l'ensemble des joueurs ayant fait match nul
        looser_list = []  # Création d'une liste contenant l'ensemble des perdants des matchs
        classement_after_round_bis = classement_after_round.copy()

        for _ in range(number_of_match // 2):
            print(f"nombre de matchs à jouer dans ce round: {number_of_match // 2}\n")
            if pause_tournoi() is False:
                round_obj.matchs = round_match_list
                tournament.list_of_round.append(round_obj)
                save_data(tournament, "data_base_tournament.json")
                return

            display_information_round(tournament)
            # Sélection aléatoire de 2 joueurs dans la copie de la liste "classement_after_round_bis"
            match_after_round = match_after_first_round(classement_after_round_bis, matches_played_round)
            if match_after_round is None:
                display_no_possible_match()
            else:
                # Affichage des joueurs du match
                display_match_information(match_after_round)

                # choix des couleurs
                choice_white_or_black(match_after_round.players)
                # Ajout du match qui vient d'être crée juste au-dessus dans la liste de tous les matchs du round
                round_match_list.append(match_after_round)
                save_data(tournament, "data_base_tournament.json")  # Enregistrement des données du tournoi

                # GESTION DES GAGNANT/PERDANT/MATCH NUL
                resultat_after_first_round = gestion_gagnant_perdant(
                    match_after_round, tournament, winner_list, draw_list, looser_list
                )

        if round_match_list:
            round_obj.matchs = round_match_list
            round_obj.date_and_hour_of_end = datetime.datetime.now()
            tournament.list_of_round.append(round_obj)
            save_data(tournament, "data_base_tournament.json")
            display_end_round(tournament, round_obj)
        else:
            display_no_match_played_in_this_round()
            return

    display_classement_apres_round(round_obj)
    classement_after_round = classement(
        resultat_after_first_round[0],
        resultat_after_first_round[1],
        resultat_after_first_round[2],
    )
    save_data(tournament, "data_base_tournament.json")
    display_finish_tournament(tournament.number_of_round)


if __name__ == "__main__":
    lancer_creation_tournoi()
