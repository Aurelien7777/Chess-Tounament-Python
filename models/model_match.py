

class Match:
    #Un tuple contenant 2 listes contenant elles-mêmes un joueur et un score
    def __init__(self, players, score):
        self.players = players # Paire de joueurs (liste ou tuple)
        self.score  = score #1 point victoire / 0 point défaite / 0.5 point match nul
        
    def __repr__(self):
        return f"Match(Joueurs={self.players},score={self.score}"
