import datetime


class Round:
    def __init__(self, matchs, name_round, date_of_start, date_of_end):
        """Modèle de données pour un tour dans un tournoi."""

        self.matchs = matchs  # Liste de matchs
        self.name_round = name_round
        self.date_and_hour_of_start = datetime.datetime.now()
        self.date_and_hour_of_end = datetime.datetime.now()


def __repr__(self):
    """Représentation textuelle de l'objet Round pour le débogage."""

    return (
        f"Round(matchs={self.matchs},\n"
        f"      nom du tour={self.name_round},\n"
        f"      date et heure de début={self.date_and_hour_of_start},\n"
        f"      date et heure de fin={self.date_and_hour_of_end})"
    )
