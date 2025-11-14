

class Match:
    """Classe représentant un match entre deux joueurs."""
    
    def __init__(self, players, score):
        self.players = players # Paire de joueurs (liste ou tuple)
        self.score  = score #1 point victoire / 0 point défaite / 0.5 point match nul
        
    def __repr__(self):
        """Représentation textuelle de l'objet Match pour le débogage."""
        
        return f"Match = {self.players}"# ,score={self.score}"
    
    
