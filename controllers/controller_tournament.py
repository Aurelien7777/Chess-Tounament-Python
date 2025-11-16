from models.model_tournament import Tournament
from views.view_tournament import (
    display_name_of_tournament,
    display_place,
    display_date_of_start,
    display_date_of_end,
    display_description,
    display_save_tournament,
)
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage


# CREATION DE TOURNOI
def create_tournament():
    """Crée un objet Tournament en demandant les informations à l'utilisateur via des vues."""

    name_of_tournament = display_name_of_tournament().strip()
    place = display_place().strip()
    date_of_start = display_date_of_start().strip()
    date_of_end = display_date_of_end().strip()
    description = display_description().strip()

    while not name_of_tournament or not place or not date_of_start or not date_of_end:
        print(
            "ERREUR: Le nom, le lieu, la date de début et la date de fin du tournoi ne peuvent pas être vides."
        )
        if not name_of_tournament:
            name_of_tournament = display_name_of_tournament().strip()
        if not place:
            place = display_place().strip()
        if not date_of_start:
            date_of_start = display_date_of_start().strip()
        if not date_of_end:
            date_of_end = display_date_of_end().strip()

    actual_round = ""

    tournament = Tournament(
        name_of_tournament=name_of_tournament,
        place=place,
        date_of_start=date_of_start,
        date_of_end=date_of_end,
        description=description,
        actual_round=actual_round,
        list_of_round=[],
        list_player_saved=[],  #
    )

    return tournament


def serializer_tournament(obj):
    """Sérialise un objet Tournament en dictionnaire pour la sauvegarde dans TinyDB."""

    if isinstance(
        obj, Tournament
    ):  # Vérification que l'objet de classe crée "obj" est bien du même type que Tournament

        def player_to_dict(player):
            """Convertit un objet Player en dictionnaire."""

            return {
                "name": player.name,
                "last_name": player.last_name,
                "date_of_birth": player.date_of_birth,
                "id": player.id,
                "score": player.score,
            }

        def match_to_dict(match):
            """Convertit un objet Match en dictionnaire."""

            return {
                "Joueurs": [
                    {
                        "name": match.players[0].name,
                        "last_name": match.players[0].last_name,
                        "id": match.players[0].id,
                        # "score": match.players[0].score
                    },
                    {
                        "name": match.players[1].name,
                        "last_name": match.players[1].last_name,
                        "id": match.players[1].id,
                        # "score": match.players[1].score
                    },
                ],
                "Score": match.score,
            }

        def round_to_dict(round_obj):
            """Convertit un objet Round en dictionnaire."""

            return {
                "Nom du round": round_obj.name_round,
                "Date de début": str(round_obj.date_and_hour_of_start),
                "Date de fin": str(round_obj.date_and_hour_of_end),
                "Matchs": [match_to_dict(m) for m in round_obj.matchs],
            }

        # Sérialisation de l'objet Tournament en dictionnaire
        data_tournament = {
            "Nom du tournoi": obj.name_of_tournament,
            "Lieu du tournoi": obj.place,
            "Date de début du tournoi": obj.date_of_start,
            "Date de fin du tournoi": obj.date_of_end,
            "Nombre de round": obj.number_of_round,
            "Informations des tours": [round_to_dict(r) for r in obj.list_of_round],
            "Liste des joueurs": [player_to_dict(p) for p in obj.list_player_saved],
            "Description": obj.description,
        }
        return data_tournament
    raise TypeError(f"Type non sérialisable: {type(obj)}")


def save_data(data_tournament, data_base_tournament):
    """Sauvegarde les données du tournoi dans la base de données TinyDB."""

    db = TinyDB(
        data_base_tournament,
        storage=JSONStorage,
        ensure_ascii=False,
        indent=2,
        encoding="utf-8",
    )

    # Conversion des données en dictionnaire
    data = serializer_tournament(
        data_tournament
    )  # Sérialisation de l'objet python Tournament en dictionnaire pour quelle puisse être stockée dans TinyDB.

    request_tournament = Query()  # L'objet utilisé pour créer les requêtes

    request_data_tournament = (
        request_tournament["Nom du tournoi"] == data["Nom du tournoi"]
    )  # Requête pour vérifier si le tournoi existe déjà dans la base de données TinyDB.

    existing = db.get(
        request_data_tournament
    )  # Vérifie si le tournoi existe déjà dans la base de données TinyDB.
    if (
        not existing
    ):  # Si le tournoi n'existe pas encore dans la base de données TinyDB.
        db.insert(data)  # Insère les données du tournoi dans la base de données TinyDB.
        display_save_tournament(data)

    else:
        db.update(
            {"Liste des joueurs": data["Liste des joueurs"]}, request_data_tournament
        )
        db.update(
            {"Informations des tours": data["Informations des tours"]},
            request_data_tournament,
        )  # Mise à jour des informations des tours contenant des objets Match sérialisés.
        db.update({"Description": data["Description"]}, request_data_tournament)
        db.update({"Lieu du tournoi": data["Lieu du tournoi"]}, request_data_tournament)
        db.update(
            {"Date de début du tournoi": data["Date de début du tournoi"]},
            request_data_tournament,
        )
        db.update(
            {"Date de fin du tournoi": data["Date de fin du tournoi"]},
            request_data_tournament,
        )
        db.update({"Nombre de round": data["Nombre de round"]}, request_data_tournament)
        # display_update_tournament()

    db.close()
    return data_base_tournament


def charger_tournoi_par_nom(data_base_tournament_path, nom_tournoi):
    """Charge un tournoi à partir de son nom dans la base de données TinyDB."""

    db = TinyDB(
        data_base_tournament_path,
        storage=JSONStorage,
        ensure_ascii=False,
        indent=2,
        encoding="utf-8",
    )
    object_request_tournoi = (
        Query()
    )  # Query est une classe de TinyDB qui permet de construire des requêtes pour interroger la base de données.
    request_tournoi = db.get(
        object_request_tournoi["Nom du tournoi"] == nom_tournoi
    )  # db.get va rechercher le 1er élément qui correspond à la requête dans le fichier JSON.
    db.close()
    if not request_tournoi:
        return None

    # création de l'objet Tournament à partir des données chargées
    tournoi = Tournament(
        name_of_tournament=request_tournoi["Nom du tournoi"],
        place=request_tournoi["Lieu du tournoi"],
        date_of_start=request_tournoi["Date de début du tournoi"],
        date_of_end=request_tournoi["Date de fin du tournoi"],
        description=request_tournoi["Description"],
        actual_round="",
        list_of_round=[],
        list_player_saved=[],
    )
    tournoi.number_of_round = request_tournoi["Nombre de round"]
    return tournoi, request_tournoi
    # Les données retounrées sont sous forme de dictionnaire et non pas d'objets Tournament, Round, Match ou Player.
    # C'est ce qu'on appelle une désérialisation. Passer de dictionnaire à des objets.
    # On retourne request_tournoi pour récupérer les listes imbriquées (list_of_round et list_player_saved).
