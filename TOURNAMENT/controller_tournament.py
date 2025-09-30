from views.view import display_name, display_menu, display_lastname, display_date_of_birth, display_id,display_created_player
from views.view import display_player_add_to_match
from models.model import Player
from TOURNAMENT.model_tournament import Tournament, Round, Match
from TOURNAMENT.view_tournament import display_name_of_tournament, display_place, display_date_of_start, display_date_of_end, display_description, display_actual_round
from controllers.controller import create_player

#CREATION DE TOURNOI
def create_tournament():
    name_of_tournament = display_name_of_tournament()
    place = display_place()
    date_of_start = display_date_of_start()
    date_of_end = display_date_of_end()
    description = display_description()
    actual_round = display_actual_round()
    tournament = Tournament(name_of_tournament=name_of_tournament,place=place,date_of_start=date_of_start,date_of_end=date_of_end,
                            description=description, actual_round=actual_round, number_of_round=4
                            ,list_of_round=[], list_player_saved=[]) 
    return tournament



#CREATION TOURNAMENT
def manage_create_tournament():
    create_tournament()
    
    
    
"""elif choice == 3: 
    manage_create_tournament()"""


