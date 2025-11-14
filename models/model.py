
class Player:
    def __init__(self, name, last_name, date_of_birth, id, score):
        """Initialise un joueur avec les informations fournies."""
        
        self.name = name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.id = id #L'ID ne doit pas être généré
        self.score = score
    def __repr__(self):
        """Représentation textuelle de l'objet Player pour le débogage."""
        
        return f"Player(nom={self.name},prenom={self.last_name} ,date de naissance={self.date_of_birth}, ID={self.id}, score={self.score})"