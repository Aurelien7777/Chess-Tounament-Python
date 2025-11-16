# ============================================================================
# IMPORTS
# ============================================================================
import datetime

# Local imports
from models.model_match import Match
from models.model_round import Round
from controllers.controller import charger_joueurs, save_score, joueurs_du_tournoi
from controllers.controller_tournament import save_data, charger_tournoi_par_nom
from controllers.controller_match import manage_winner_match_bis, choice_white_or_black
from controllers.controller_round import reconstruire_rounds
from views.view_reprise_tournoi import (
    display_rebuild_round,
    display_initialisation_played_pairs,
    display_pause_tournament,
    display_no_possible_match,
    display_end_round,
    display_no_match_played_in_this_round,
    request_name_tournament_resume,
    display_player_draws,
    display_player_wins,
    display_player_loses,
    display_tournament_finished,
    display_final_classement,
    display_player_final_ranking,
    display_end_of_round,
    display_classement_apres_round,
    display_player_ranking_after_round,
    display_tournament_not_found,
    display_number_of_match,
    display_matches_played,
    display_remaining_matches,
    display_start_round,
    display_match_count,
    display_match_information,
    display_match_opponent,
    request_continue_tournament,
)


def resume_tournament():

    global data_tournament, objet_name_tournament, joueurs_par_id
    global rebuilding_rounds, all_players, number_of_match

    # ============================================================================
    # REPRISE D'UN ROUND INCOMPLET
    # ============================================================================
    def resume_incomplete_round():
        """Reprendre un round incomplet"""

        display_rebuild_round(rebuilding_rounds)
        round_obj = rebuilding_rounds[-1]
        data_tournament.actual_round = round_obj.name_round
        current_round_index = len(rebuilding_rounds) - 1
        round_match_list = round_obj.matchs.copy()

        return round_obj, current_round_index, round_match_list

    def initialize_matches_played(round_match_list):
        """Initialiser les paires déjà jouées dans le round en cours"""

        display_initialisation_played_pairs()
        matches_played_this_round = []
        for match_round in round_match_list:
            match_key = tuple(
                sorted((match_round.players[0].id, match_round.players[1].id))
            )
            matches_played_this_round.append(match_key)
        return matches_played_this_round

    # ============================================================================
    # REPRISE D'UN ROUND COMPLET
    # ============================================================================
    def create_new_round(current_round_index):
        """Créer un nouveau round"""
        # construire le nouveau round
        return Round(
            matchs=[],
            name_round=f"Round {current_round_index + 1}",
            date_of_start=datetime.datetime.now(),
            date_of_end=None,
        )

    # =============================================================================
    # LANCER LES MATCHS RESTANT DU ROUND
    # =============================================================================
    def pause_tournoi():
        """Proposer de faire une pause dans le tournoi"""

        ask_for_continue = request_continue_tournament()
        if ask_for_continue != "oui":
            display_pause_tournament()
            return False

    def save_round_state(round_obj, round_match_list):
        """Sauvegarder l'état du round en cours"""

        round_obj.matchs = round_match_list
        if round_obj not in data_tournament.list_of_round:
            data_tournament.list_of_round.append(round_obj)
        save_data(data_tournament, "data_base_tournament.json")

    def update_classement_and_available_players(
        classement_after_round, matches_played_this_round
    ):
        """Mettre à jour le classement et la liste des joueurs disponibles pour le round en cours"""

        already_played = []  # liste des joueurs ayant déjà joué dans CE roundo
        for game_key in matches_played_this_round:
            already_played.append(game_key[0])
            already_played.append(game_key[1])

        # joueurs disponibles
        classement_disponible = []
        for gamer in classement_after_round:  # parcourir le classement
            if (
                gamer.id not in already_played
            ):  # si le joueur n'a pas encore joué dans CE round
                classement_disponible.append(gamer)  # ajouter aux joueurs dispo
        if len(classement_disponible) < 2:  # pas assez de joueurs dispo
            classement_disponible = classement_after_round[
                :
            ]  # reset si plus assez de joueurs dispo

        return classement_disponible

    def research_pair_no_played(classement_disponible, matches_played_this_round):
        """Rechercher une paire de joueurs n'ayant pas encore joué ensemble dans CE round"""

        match_after_round = None
        index_de_recherche = 0
        while index_de_recherche < len(
            classement_disponible
        ):  # tant que l'index de recherche est inférieur au nombre de joueurs dispo
            search_next_player = index_de_recherche + 1  # chercher le joueur suivant
            while search_next_player < len(
                classement_disponible
            ):  # tant que l'index du joueur suivant est inférieur au nombre de joueurs dispo
                player_1 = classement_disponible[index_de_recherche]  # joueur courant
                player_2 = classement_disponible[search_next_player]  # joueur suivant
                game_key = tuple(
                    sorted((player_1.id, player_2.id))
                )  # clé du match à tester
                if (
                    game_key not in matches_played_this_round
                ):  # si la paire n'a pas encore joué dans CE round
                    match_after_round = Match(
                        players=[player_1, player_2], score=[0, 0]
                    )  # créer le match
                    matches_played_this_round.append(
                        game_key
                    )  # ajouter la paire aux matchs joués dans CE round
                    break
                search_next_player += 1
            if match_after_round is not None:
                break
            index_de_recherche += 1
        return match_after_round

    # clôture du round si plus de match possible
    def closing_round_if_no_match(round_obj, round_match_list):
        """Clôturer le round si plus de match possible"""

        display_no_possible_match()
        # clôturer le round courant
        if round_match_list:
            round_obj.matchs = round_match_list
            round_obj.date_and_hour_of_end = datetime.datetime.now()
            if round_obj not in data_tournament.list_of_round:
                data_tournament.list_of_round.append(round_obj)
            display_end_round(data_tournament, round_obj)
        else:
            display_no_match_played_in_this_round()
        save_data(data_tournament, "data_base_tournament.json")
        return

    # gestion du résultat
    def manage_match(match_after_round):
        """Gestion du résultat d'un match"""

        winner = manage_winner_match_bis(match_after_round.players)
        score1, score2 = 0, 0
        if isinstance(winner, list):
            score1 = score2 = 0.5
            display_player_draws()
        elif winner[0] is match_after_round.players[0]:
            score1, score2 = 1, 0
            display_player_wins(winner)
        else:
            score1, score2 = 0, 1
            display_player_loses(winner)
        match_after_round.score = [score1, score2]

        save_score("data_base_players.json", all_players)
        # utilisation de key qui permet de trier selon un attribut spécifique déterminé grâce à une fonction lambda.
        # Fonction lambda qui prend un joueur en entrée et renvoie son score.
        classement_after_round = sorted(
            all_players,
            key=lambda player_in_classement: player_in_classement.score,
            reverse=True,
        )

        return classement_after_round

    def verify_tournament_completion():
        """Vérifier si le tournoi est terminé et afficher le classement final"""

        if len(data_tournament.list_of_round) >= data_tournament.number_of_round:
            display_tournament_finished(data_tournament)

            display_final_classement()
            classement_final = sorted(
                all_players,
                key=lambda player_in_classement: player_in_classement.score,
                reverse=True,
            )
            for idx, player in enumerate(classement_final, 1):
                display_player_final_ranking(idx, player)
            return True
        return False

    def closing_round_normal(round_obj, round_match_list):
        """Clôturer un round terminé normalement."""

        round_obj.matchs = round_match_list
        round_obj.date_and_hour_of_end = datetime.datetime.now()

        if round_obj not in data_tournament.list_of_round:
            data_tournament.list_of_round.append(round_obj)

        display_end_of_round(data_tournament, round_obj)
        display_classement_apres_round(data_tournament)
        classement_apres = sorted(
            all_players,
            key=lambda player_in_classement: player_in_classement.score,
            reverse=True,
        )
        for idx, player in enumerate(classement_apres, 1):
            display_player_ranking_after_round(idx, player)

        save_data(data_tournament, "data_base_tournament.json")

    # ============================================================================
    # REPRENDRE UN TOURNOI EXISTANT
    # ============================================================================

    name_tournament_resume = request_name_tournament_resume()
    loading_tournament = charger_tournoi_par_nom(
        "data_base_tournament.json", name_tournament_resume
    )
    if not loading_tournament:
        display_tournament_not_found()
        return

    # Charger le tournoi (depuis la base tournois)
    data_tournament, objet_name_tournament = loading_tournament

    # Charger tous les joueurs (depuis la base joueurs)
    joueurs_par_id = charger_joueurs("data_base_players.json")

    # Reconstruire les rounds + paires déjà jouées
    rebuilding_rounds = reconstruire_rounds(objet_name_tournament, joueurs_par_id)

    # Lister les joueurs de CE tournoi (objets Player)
    all_players = joueurs_du_tournoi(objet_name_tournament, joueurs_par_id)

    # Réinjecter l'état dans l'objet tournoi
    data_tournament.list_of_round = rebuilding_rounds
    number_of_match = len(all_players) // 2
    display_number_of_match(number_of_match)

    # =============================================================================
    # REPRENDRE UN ROUND COMPLET OU NON
    # =============================================================================

    # Dans le cas où le dernier round est incomplet, on le reprend
    while True:

        if (
            rebuilding_rounds and len(rebuilding_rounds[-1].matchs) < number_of_match
        ):  # si le nombre de matchs joués dans le dernier round est inférieur au nombre de matchs total prévu.
            # Vérification effectuée uniquement si rebuilding_rounds n'est pas vide.
            round_obj, current_round_index, round_match_list = resume_incomplete_round()
            remaining_matches = number_of_match - len(round_match_list)
            display_matches_played(round_match_list, number_of_match)
            display_remaining_matches(remaining_matches)

            matches_played_this_round = initialize_matches_played(round_match_list)
            classement_after_round = sorted(
                all_players,
                key=lambda player_in_classement: player_in_classement.score,
                reverse=True,
            )

        # sinon, créer un nouveau round
        else:
            current_round_index = len(rebuilding_rounds)
            if current_round_index >= data_tournament.number_of_round:
                # tournoi déjà terminé : on affiche le classement final et on sort
                verify_tournament_completion()
                break

            # construire le nouveau round
            round_obj = create_new_round(current_round_index)
            # mettre à jour le round actuel dans le tournoi
            data_tournament.actual_round = round_obj.name_round
            display_start_round(round_obj)

            # initialiser les variables du round
            round_match_list = []
            remaining_matches = number_of_match
            matches_played_this_round = []
            classement_after_round = sorted(
                all_players,
                key=lambda player_in_classement: player_in_classement.score,
                reverse=True,
            )

        # =============================================================================
        # LANCER LES MATCHS RESTANT DU ROUND
        # =============================================================================
        for _ in range(remaining_matches):
            if pause_tournoi() is False:
                save_data(data_tournament, "data_base_tournament.json")
                return

            if round_match_list:
                save_round_state(round_obj, round_match_list)

            classement_disponible = update_classement_and_available_players(
                classement_after_round, matches_played_this_round
            )
            # chercher une paire non jouée dans CE round
            match_after_round = research_pair_no_played(
                classement_disponible, matches_played_this_round
            )

            # clôture du round si plus de match possible
            if match_after_round is None:
                closing_round_if_no_match(round_obj, round_match_list)
                break

            # sinon, gérer le match
            choice_white_or_black(match_after_round.players)
            round_match_list.append(match_after_round)

            # Afficher le nombre de match en cours
            display_match_count(round_match_list, number_of_match)

            # Afficher les informations du match
            display_match_information(match_after_round)
            display_match_opponent(match_after_round)

            classement_after_round = manage_match(match_after_round)

        # Clôture normale si tous les matchs joués
        if len(round_match_list) == number_of_match:
            closing_round_normal(round_obj, round_match_list)

        # Si tournoi terminé, on sort
        if verify_tournament_completion():
            break

        # préparer la prochaine itération
        # rebuilding_rounds = data_tournament.list_of_round

    save_data(data_tournament, "data_base_tournament.json")
