import os
from routes import route
from world_map_objects import world_map_object
from pokemon import pokemon
import keyboard
import random
import pdb



def display_combat(world_map_object, player_position, pokemon, route, section, encounter_pokemon, encounter_level) :    
    os.system("cls" if os.name == "nt" else "clear")  # Clear the console screen
    
    for obj in pokemon:
        if obj['name'] == encounter_pokemon:
            print (obj['sprite_front'])            
    
    print ("Press C to return to map")

    while True:
        if keyboard.is_pressed('c'):        
            return    
