# ============================================================================
# IMPORTS
# ============================================================================
import datetime

# Local imports
from models.model_match import Match
from models.model_round import Round
from controllers.controller import (
    DataBasePlayerController,
    TournamentDataManager,
    PlayerController,
)

from controllers.controller_tournament import TournamentController
from controllers.controller_match import MatchController
from controllers.controller_round import RoundController
from views.view_reprise_tournoi import (
    RoundViewRepriseTournoi,
    ResultatViewRepriseTournoi,
    TournamentResumeView,
    MatchViewRepriseTournoi,
    ClassementViewRepriseTournoi,
)


class TournamentResumeOrchestrator:
    @staticmethod
    def resume_tournament():

        global data_tournament, objet_name_tournament, joueurs_par_id
        global rebuilding_rounds, all_players, number_of_match

        # ============================================================================
        # REPRISE D'UN ROUND INCOMPLET
        # ============================================================================
        class RoundResumeManager:
            @staticmethod
            def resume_incomplete_round():
                """Reprendre un round incomplet"""

                RoundViewRepriseTournoi.display_rebuild_round(rebuilding_rounds)
                round_obj = rebuilding_rounds[-1]
                data_tournament.actual_round = round_obj.name_round
                current_round_index = len(rebuilding_rounds) - 1
                round_match_list = round_obj.matchs.copy()

                return round_obj, current_round_index, round_match_list

            @staticmethod
            def initialize_matches_played(round_match_list):
                """Initialiser les paires déjà jouées dans le round en cours"""

                MatchViewRepriseTournoi.display_initialisation_played_pairs()
                matches_played_this_round = []
                for match_round in round_match_list:
                    match_key = tuple(
                        sorted((match_round.players[0].id, match_round.players[1].id))
                    )
                    matches_played_this_round.append(match_key)
                return matches_played_this_round

            @staticmethod
            def create_new_round(current_round_index):
                """Créer un nouveau round"""

                return Round(
                    matchs=[],
                    name_round=f"Round {current_round_index + 1}",
                    date_of_start=datetime.datetime.now(),
                    date_of_end=None,
                )

        # =============================================================================
        # LANCER LES MATCHS RESTANT DU ROUND
        # =============================================================================
        class TournamentStateManager:
            @staticmethod
            def pause_tournoi():
                """Proposer de faire une pause dans le tournoi"""

                ask_for_continue = TournamentResumeView.request_continue_tournament()
                if ask_for_continue != "oui":
                    TournamentResumeView.display_pause_tournament()
                    return False

            @staticmethod
            def save_round_state(round_obj, round_match_list):
                """Sauvegarder l'état du round en cours"""

                round_obj.matchs = round_match_list
                if round_obj not in data_tournament.list_of_round:
                    data_tournament.list_of_round.append(round_obj)
                TournamentController.save_data(
                    data_tournament, "data_base_tournament.json"
                )

            @staticmethod
            def verify_tournament_completion():
                """Vérifier si le tournoi est terminé et afficher le classement final"""

                if (
                    len(data_tournament.list_of_round)
                    >= data_tournament.number_of_round
                ):
                    TournamentResumeView.display_tournament_finished(data_tournament)

                    ClassementViewRepriseTournoi.display_final_classement()
                    classement_final = sorted(
                        all_players,
                        key=lambda player_in_classement: player_in_classement.score,
                        reverse=True,
                    )
                    for idx, player in enumerate(classement_final, 1):
                        ClassementViewRepriseTournoi.display_player_final_ranking(
                            idx, player
                        )
                    return True
                return False

        class MatchPairingManager:
            @staticmethod
            def update_classement_and_available_players(
                classement_after_round, matches_played_this_round
            ):
                """Mettre à jour le classement et la liste des joueurs disponibles pour le round en cours"""

                already_played = []  # liste des joueurs ayant déjà joué dans ce round
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

            @staticmethod
            def research_pair_no_played(
                classement_disponible, matches_played_this_round
            ):
                """Rechercher une paire de joueurs n'ayant pas encore joué ensemble dans CE round"""

                match_after_round = None
                index_de_recherche = 0
                while index_de_recherche < len(
                    classement_disponible
                ):  # tant que l'index de recherche est inférieur au nombre de joueurs dispo
                    search_next_player = (
                        index_de_recherche + 1
                    )  # chercher le joueur suivant
                    while search_next_player < len(
                        classement_disponible
                    ):  # tant que l'index du joueur suivant est inférieur au nombre de joueurs dispo
                        player_1 = classement_disponible[
                            index_de_recherche
                        ]  # joueur courant
                        player_2 = classement_disponible[
                            search_next_player
                        ]  # joueur suivant
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

        class MatchResultManager:
            @staticmethod
            def manage_match(match_after_round):
                """Gestion du résultat d'un match"""

                winner = MatchController.manage_winner_match_bis(
                    match_after_round.players
                )
                score1, score2 = 0, 0
                if isinstance(winner, list):
                    score1 = score2 = 0.5
                    ResultatViewRepriseTournoi.display_player_draws()
                elif winner[0] is match_after_round.players[0]:
                    score1, score2 = 1, 0
                    ResultatViewRepriseTournoi.display_player_wins(winner)
                else:
                    score1, score2 = 0, 1
                    ResultatViewRepriseTournoi.display_player_loses(winner)
                match_after_round.score = [score1, score2]

                DataBasePlayerController.save_score(
                    "data_base_players.json", all_players
                )

                classement_after_round = sorted(
                    all_players,
                    key=lambda player_in_classement: player_in_classement.score,
                    reverse=True,
                )

                return classement_after_round

        class RoundClosureManager:
            @staticmethod
            def closing_round_normal(round_obj, round_match_list):
                """Clôturer un round terminé normalement."""

                round_obj.matchs = round_match_list
                round_obj.date_and_hour_of_end = datetime.datetime.now()

                if round_obj not in data_tournament.list_of_round:
                    data_tournament.list_of_round.append(round_obj)

                RoundViewRepriseTournoi.display_end_round(data_tournament, round_obj)
                ClassementViewRepriseTournoi.display_classement_apres_round(
                    data_tournament
                )
                classement_apres = sorted(
                    all_players,
                    key=lambda player_in_classement: player_in_classement.score,
                    reverse=True,
                )
                for idx, player in enumerate(classement_apres, 1):
                    ClassementViewRepriseTournoi.display_player_ranking_after_round(
                        idx, player
                    )

                TournamentController.save_data(
                    data_tournament, "data_base_tournament.json"
                )

            @staticmethod
            def closing_round_if_no_match(round_obj, round_match_list):
                """Clôturer le round si plus de match possible"""

                MatchViewRepriseTournoi.display_no_possible_match()
                if round_match_list:
                    round_obj.matchs = round_match_list
                    round_obj.date_and_hour_of_end = datetime.datetime.now()
                    if round_obj not in data_tournament.list_of_round:
                        data_tournament.list_of_round.append(round_obj)
                    RoundViewRepriseTournoi.display_end_round(
                        data_tournament, round_obj
                    )
                else:
                    MatchViewRepriseTournoi.display_no_match_played_in_this_round()
                TournamentController.save_data(
                    data_tournament, "data_base_tournament.json"
                )
                return

        # ============================================================================
        # REPRENDRE UN TOURNOI EXISTANT
        # ============================================================================

        name_tournament_resume = TournamentResumeView.request_name_tournament_resume()
        loading_tournament = TournamentController.charger_tournoi_par_nom(
            "data_base_tournament.json", name_tournament_resume
        )
        if not loading_tournament:
            TournamentResumeView.display_tournament_not_found()
            return

        """ Charger le tournoi (depuis la base tournois)"""
        data_tournament, objet_name_tournament = loading_tournament

        """ Charger tous les joueurs (depuis la base joueurs)"""
        joueurs_par_id = PlayerController.charger_joueurs("data_base_players.json")

        """ Reconstruire les rounds + paires déjà jouées"""
        rebuilding_rounds = RoundController.reconstruire_rounds(
            objet_name_tournament, joueurs_par_id
        )

        """ Lister les joueurs de CE tournoi (objets Player)"""
        all_players = TournamentDataManager.joueurs_du_tournoi(
            objet_name_tournament, joueurs_par_id
        )

        """ Réinjecter l'état dans l'objet tournoi"""
        data_tournament.list_of_round = rebuilding_rounds
        number_of_match = len(all_players) // 2
        MatchViewRepriseTournoi.display_number_of_match(number_of_match)

        # =============================================================================
        # REPRENDRE UN ROUND COMPLET OU NON
        # =============================================================================

        """Dans le cas où le dernier round est incomplet, on le reprend"""
        while True:

            if (
                rebuilding_rounds
                and len(rebuilding_rounds[-1].matchs) < number_of_match
            ):
                round_obj, current_round_index, round_match_list = (
                    RoundResumeManager.resume_incomplete_round()
                )
                remaining_matches = number_of_match - len(round_match_list)
                MatchViewRepriseTournoi.display_matches_played(
                    round_match_list, number_of_match
                )
                MatchViewRepriseTournoi.display_remaining_matches(remaining_matches)

                matches_played_this_round = (
                    RoundResumeManager.initialize_matches_played(round_match_list)
                )
                classement_after_round = sorted(
                    all_players,
                    key=lambda player_in_classement: player_in_classement.score,
                    reverse=True,
                )

            # sinon, créer un nouveau round
            else:
                current_round_index = len(rebuilding_rounds)
                if current_round_index >= data_tournament.number_of_round:
                    TournamentStateManager.verify_tournament_completion()
                    break

                """ construire le nouveau round"""
                round_obj = RoundResumeManager.create_new_round(current_round_index)
                """ mettre à jour le round actuel dans le tournoi"""
                data_tournament.actual_round = round_obj.name_round
                RoundViewRepriseTournoi.display_start_round(round_obj)

                """ initialiser les variables du round"""
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
                if TournamentStateManager.pause_tournoi() is False:
                    TournamentController.save_data(
                        data_tournament, "data_base_tournament.json"
                    )
                    return

                if round_match_list:
                    TournamentStateManager.save_round_state(round_obj, round_match_list)

                classement_disponible = (
                    MatchPairingManager.update_classement_and_available_players(
                        classement_after_round, matches_played_this_round
                    )
                )
                # chercher une paire non jouée dans CE round
                match_after_round = MatchPairingManager.research_pair_no_played(
                    classement_disponible, matches_played_this_round
                )

                """ clôture du round si plus de match possible"""
                if match_after_round is None:
                    RoundClosureManager.closing_round_if_no_match(
                        round_obj, round_match_list
                    )
                    break

                """ sinon, gérer le match"""
                MatchController.choice_white_or_black(match_after_round.players)
                round_match_list.append(match_after_round)

                """ Afficher le nombre de match en cours"""
                MatchViewRepriseTournoi.display_match_count(
                    round_match_list, number_of_match
                )

                """ Afficher les informations du match"""
                MatchViewRepriseTournoi.display_match_information(match_after_round)
                MatchViewRepriseTournoi.display_match_opponent(match_after_round)

                classement_after_round = MatchResultManager.manage_match(
                    match_after_round
                )

            """#Clôture normale si tous les matchs joués"""
            if len(round_match_list) == number_of_match:
                RoundClosureManager.closing_round_normal(round_obj, round_match_list)

            """# Si tournoi terminé, on sort"""
            if TournamentStateManager.verify_tournament_completion():
                break

        TournamentController.save_data(data_tournament, "data_base_tournament.json")
