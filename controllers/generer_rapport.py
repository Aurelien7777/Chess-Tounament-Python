from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from views.view_report import (
    MenuViewReport,
    SortedPlayersViewReport,
    RoundsAndMatchesViewReport,
    TournamentViewReport,
)


def generate_player_tournament_report(
    data_base_tournament_path="data_base_tournament.json",
):
    """Génère un rapport des joueurs d'un tournoi spécifique triés par nom."""

    name_tournament_resume = TournamentViewReport.display_get_tournament_name()

    if not name_tournament_resume:
        TournamentViewReport.display_ask_tournament_name()
        return

    db = TinyDB(
        data_base_tournament_path,
        storage=JSONStorage,
        ensure_ascii=False,
        indent=2,
        encoding="utf-8",
    )
    object_request_tournoi = Query()

    # db.get va rechercher un tournoi possédant le même nom que celui entré par l'utilisateur
    request_tournoi = db.get(
        object_request_tournoi["Nom du tournoi"] == name_tournament_resume
    )

    if request_tournoi is None:
        TournamentViewReport.display_if_tournament_not_found(name_tournament_resume)
        db.close()
        return

    liste_joueurs_triee = sorted(
        request_tournoi["Liste des joueurs"],
        key=lambda name_player: name_player["name"],
    )
    for joueur in liste_joueurs_triee:
        SortedPlayersViewReport.display_sorted_players(joueur)

    db.close()


def generate_all_player_report(data_base_players_path="data_base_players.json"):
    """Génère un rapport de tous les joueurs disponibles dans la base de données."""

    db = TinyDB(
        data_base_players_path,
        storage=JSONStorage,
        ensure_ascii=False,
        indent=2,
        encoding="utf-8",
    )
    all_players = db.all()

    if not all_players:
        SortedPlayersViewReport.display_no_players_found()
        db.close()
        return

    SortedPlayersViewReport.display_introduction_available_players()
    liste_all_players_triee = sorted(
        all_players, key=lambda name_player: name_player["name"]
    )
    for joueur in liste_all_players_triee:
        SortedPlayersViewReport.display_sorted_players(joueur)

    db.close()


def generate_tournament_report(data_base_tournament_path="data_base_tournament.json"):
    """Génère un rapport de tous les tournois disponibles dans la base de données."""

    db = TinyDB(
        data_base_tournament_path,
        storage=JSONStorage,
        ensure_ascii=False,
        indent=2,
        encoding="utf-8",
    )
    all_tournaments = db.all()

    if not all_tournaments:
        TournamentViewReport.display_if_tournament_not_found()
        db.close()
        return

    TournamentViewReport.display_introduction_available_tournaments()
    for tournoi in all_tournaments:
        TournamentViewReport.display_all_tournaments(tournoi)

    db.close()


def generate_name_and_date_tournament_report(
    data_base_tournament_path="data_base_tournament.json",
):
    """Génère un rapport des noms et dates d'un tournoi'donné."""

    name_tournament = TournamentViewReport.display_get_tournament_name()
    if not name_tournament:
        TournamentViewReport.display_ask_tournament_name()
        return

    db = TinyDB(
        data_base_tournament_path,
        storage=JSONStorage,
        ensure_ascii=False,
        indent=2,
        encoding="utf-8",
    )
    object_request_tournoi = Query()

    # db.get va rechercher un tournoi possédant le même nom que celui entré par l'utilisateur
    request_tournoi = db.get(
        object_request_tournoi["Nom du tournoi"] == name_tournament
    )

    if request_tournoi is None:
        TournamentViewReport.display_if_tournament_not_found(name_tournament)
        db.close()
        return

    TournamentViewReport.display_introduction_tournament_with_date(request_tournoi)
    TournamentViewReport.display_tournament_with_name_and_date(request_tournoi)

    db.close()


def generate_report_all_rounds_and_all_matches_of_tournament(
    data_base_tournament_path="data_base_tournament.json",
):
    """Génère un rapport de tous les rounds et matchs d'un tournoi donné."""
    name_tournament = TournamentViewReport.display_get_tournament_name()
    if not name_tournament:
        TournamentViewReport.display_ask_tournament_name()
        return

    db = TinyDB(
        data_base_tournament_path,
        storage=JSONStorage,
        ensure_ascii=False,
        indent=2,
        encoding="utf-8",
    )
    object_request_tournoi = Query()

    # db.get va rechercher un tournoi possédant le même nom que celui entré par l'utilisateur
    request_tournoi = db.get(
        object_request_tournoi["Nom du tournoi"] == name_tournament
    )

    if request_tournoi is None:
        TournamentViewReport.display_if_tournament_not_found(name_tournament)
        db.close()
        return

    RoundsAndMatchesViewReport.display_introduction_report_rounds_and_matches(
        name_tournament
    )
    for round_info in request_tournoi["Informations des tours"]:
        RoundsAndMatchesViewReport.display_rounds_and_matches(round_info)
        for match in round_info["Matchs"]:
            player1 = match["Joueurs"][0]
            player2 = match["Joueurs"][1]
            score = match["Score"]
            RoundsAndMatchesViewReport.display_match_info(player1, player2, score)


# ======= MENU REPORT =======#
def menu_report():

    choice = int(
        MenuViewReport.display_menu_report_choice()
    )  # Récupération de la donnée entrée dans la fonction input de la fonction display_menu()
    if choice > 5 or choice < 1:
        MenuViewReport.display_error_invalid_menu_choice()
        try:
            choice = int(
                MenuViewReport.display_menu_report_choice()
            )  # Conversion en INT
        except (ValueError, TypeError, KeyboardInterrupt):
            MenuViewReport.display_error_invalid_menu_choice()

    if choice == 1:
        generate_all_player_report()

    elif choice == 2:
        generate_tournament_report()

    elif choice == 3:
        # CREATION DU TOURNOI
        generate_name_and_date_tournament_report()

    elif choice == 4:
        # Reprendre un tournoi existant
        generate_player_tournament_report()

    elif choice == 5:
        generate_report_all_rounds_and_all_matches_of_tournament()
