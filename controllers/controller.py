import random
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from models.model import Player
from views.view import PlayerView, MenuView, MessageView


class PlayerController:
    @staticmethod
    def create_player():
        """Crée un objet Player en demandant les informations à l'utilisateur via des vues."""

        list_number_for_id = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        list_letter_for_id = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "G",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        ]

        name = PlayerView.display_name().strip()
        last_name = PlayerView.display_lastname().strip()
        while not name or not last_name:
            print("ERREUR: Le nom et le prénom ne peuvent pas être vides.")
            name = str(PlayerView.display_name().strip())
            last_name = str(PlayerView.display_lastname().strip())

        date_of_birth = PlayerView.display_date_of_birth()
        while not date_of_birth:
            print("ERREUR: La date de naissance ne peut pas être vide.")
            date_of_birth = PlayerView.display_date_of_birth()

        list_for_id = random.sample(list_letter_for_id, k=2) + random.sample(
            list_number_for_id, k=5
        )
        id = "".join(list_for_id)

        player = Player(
            name=name, date_of_birth=date_of_birth, last_name=last_name, id=id, score=0
        )

        PlayerView.display_created_player(name, last_name)

        return player

    @staticmethod
    def charger_joueurs(data_base_players_path):
        """Charge les joueurs depuis la base de données TinyDB et retourne un dictionnaire de joueurs par ID."""

        data_base_player = TinyDB(
            data_base_players_path,
            storage=JSONStorage,
            ensure_ascii=False,
            indent=2,
            encoding="utf-8",
        )

        joueurs = {}

        for info_player in data_base_player.all():

            joueur = Player(
                name=info_player["name"],
                last_name=info_player["last_name"],
                date_of_birth=info_player["date_of_birth"],
                id=info_player["id"],
                score=info_player["score"],
            )
            joueurs[joueur.id] = joueur
        data_base_player.close()
        return joueurs


class DataBasePlayerController:
    @staticmethod
    def serializer(obj):
        """Convertit un objet Python en JSON"""

        if isinstance(
            obj, Player
        ):  # Vérification que l'objet de classe crée "obj" est bien du même type que Player
            data_player = {
                "name": obj.name,
                "last_name": obj.last_name,
                "date_of_birth": obj.date_of_birth,
                "id": obj.id,
                "score": obj.score,
            }
            return data_player
        raise TypeError(f"Type non sérialisable: {type(obj)}")

    @staticmethod
    def save_score(data_base_players, players):
        """Met à jour le score des joueurs dans la base de données TinyDB."""

        db = TinyDB(
            data_base_players,
            storage=JSONStorage,
            ensure_ascii=False,
            indent=2,
            encoding="utf-8",
        )
        request_player = Query()  # L'objet utilisé pour créer les requêtes

        for joueur in players:
            data_player = DataBasePlayerController.serializer(
                joueur
            )  # récupère les données joueurs dont le score actuel (modifié dans manage_winner_match)

            # Recherche le joueur dans la base par id
            request_id_player = request_player.id == data_player["id"]
            existing = db.get(request_id_player)

            if existing:
                db.update(
                    {"score": data_player["score"]}, request_id_player
                )  # Accès à la clé score du dictionnaire correspondant à l'ID du joueur concerné
                MessageView.display_updated_score(joueur)
            else:
                MessageView.display_player_not_found(joueur)

        db.close()

    @staticmethod
    def save_players(players, data_base_players):
        """Sauvegarde les joueurs dans une base de données TinyDB au format JSON."""

        data_base_players = TinyDB(
            data_base_players,
            storage=JSONStorage,
            ensure_ascii=False,
            indent=2,
            encoding="utf-8",
        )

        for player in players:
            if (
                player not in data_base_players.all()
                and player not in data_base_players.all()
            ):
                data_player = DataBasePlayerController.serializer(
                    player
                )  # Récupération et conversion des infos joueurs au format JSON
                data_base_players.insert(data_player)
            else:
                MessageView.display_player_already_exists()

        return data_base_players


class TournamentDataManager:
    @staticmethod
    def joueurs_du_tournoi(file_tournament, joueurs_par_id):
        """Récupère la liste des joueurs participant à un tournoi
        à partir des données JSON du tournoi et du dictionnaire des joueurs par ID."""

        list_tournament_player = []
        # privilégier la liste officielle du tournoi
        if file_tournament.get("Liste des joueurs"):  #
            for player_in_tournament in file_tournament["Liste des joueurs"]:
                player_id_tournament = player_in_tournament["id"]
                player_from_data_base = joueurs_par_id.get(player_id_tournament)
                if player_from_data_base:
                    list_tournament_player.append(player_from_data_base)
            return list_tournament_player

        # fallback : récupérer depuis les matchs joués
        for round_in_file_tournament in file_tournament["Informations des tours"]:
            for match_in_round in round_in_file_tournament["Matchs"]:
                for player_in_match in match_in_round["Joueurs"]:
                    player_id = player_in_match["id"]
                    player_data_base = joueurs_par_id.get(player_id)
                    if (
                        player_data_base
                        and player_data_base not in list_tournament_player
                    ):
                        list_tournament_player.append(player_data_base)
        return list_tournament_player


# ====================================
# GESTION DES CHOIX UTILISATEUR
# ====================================


class MainController:
    @staticmethod
    def handle_tournament_creation():
        """Gère la création d'un tournoi."""

        from controllers.creation_tournoi import TournamentCreationOrchestrator

        TournamentCreationOrchestrator.lancer_creation_tournoi()

    @staticmethod
    def handle_tournament_resume():
        """Gère la reprise d'un tournoi existant."""

        from controllers.reprise_tournoi import TournamentResumeOrchestrator

        TournamentResumeOrchestrator.resume_tournament()

    @staticmethod
    def handle_report():
        """Gère la génération de rapports."""

        from controllers.generer_rapport import menu_report

        menu_report()

    # =============================
    # EXECUTION DU MENU PRINCIPAL
    # =============================
    @staticmethod
    def start_menu():
        """Démarre le menu principal et gère les choix de l'utilisateur."""

        choice = 0
        while choice < 1 or choice > 3 or not isinstance(choice, int):
            try:
                choice = int(
                    MenuView.display_menu()
                )  # Récupération de la donnée entrée dans la fonction input de la fonction display_menu()
            except (ValueError, TypeError):
                MenuView.display_error_invalid_menu_choice()

        if choice == 1:
            """Créer un nouveau tournoi."""
            MainController.handle_tournament_creation()

        elif choice == 2:
            """Reprendre un tournoi existant."""
            MainController.handle_tournament_resume()

        elif choice == 3:
            """Générer des rapports."""
            MainController.handle_report()
