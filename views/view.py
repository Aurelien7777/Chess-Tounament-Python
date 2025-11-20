# ====================================
# CREATION DE JOUEUR
# ====================================


class PlayerView:
    @staticmethod
    def display_name() -> str:
        return input("Entrer le nom du joueur: ")

    @staticmethod
    def display_lastname() -> str:
        return input("Entrer le prenom du joueur: ")

    @staticmethod
    def display_date_of_birth() -> str:
        return input("Entrer la date de naissance du joueur: ")

    @staticmethod
    def display_created_player(last_name, name):
        print(f"Création du joueur {last_name} {name} réussie\n")

    @staticmethod
    def ask_player_creation():
        return input("Voulez-vous créer un nouveau joueur? Oui ou Non: ")


# ====================================
# AFFICHAGE DU MENU
# ====================================


class MenuView:
    @staticmethod
    def display_menu():
        print(
            "Bienvenue dans le menu principal de l'outil de gestion des tournois d'échecs.\n"
        )
        return int(
            input(
                "1 - Créer tournoi\n"
                "2 - Reprendre un tournoi\n"
                "3 - Générer un rapport\n"
                "Entrer votre choix: "
            )
        )

    @staticmethod
    def display_error_invalid_menu_choice():
        print("ERREUR: Le choix doit être chiffre entre 1 et 3")


# ====================================
# AFFICHAGE DES MESSAGES DE CONFIRMATION ET D'ERREUR
# ====================================


class MessageView:
    @staticmethod
    def display_save_player(player):
        print(f"\nSauvegarde du joueur {player.name} {player.last_name} effectuée")

    @staticmethod
    def display_player_already_exists():
        print("Le joueur est déjà présent dans la base de donnée")

    @staticmethod
    def display_updated_score(joueur):
        print(
            f"Score mis à jour pour {joueur.name} {joueur.last_name} : {joueur.score}"
        )

    @staticmethod
    def display_player_not_found(joueur):
        print(f"{joueur.name} {joueur.last_name} introuvable : pas de mise à jour")

    @staticmethod
    def display_error_invalid_response():
        print("ERREUR: La réponse ne peut être que Oui ou Non")
