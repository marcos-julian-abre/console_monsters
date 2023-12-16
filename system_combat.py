import os
from pokemon import pokemon as pokemon_list
import keyboard
import random
import pdb
from  visuals import name_frame, message_frame
import time



def display_combat(encounter_pokemon, encounter_level) :    
    os.system("cls" if os.name == "nt" else "clear")  # Clear the console screen
    pokemon = []
    
    for obj in pokemon_list:
        if obj['name'] == encounter_pokemon:
            pokemon = obj
    

    name_frame(pokemon["name"])    
    print(pokemon["sprite_front"])
    print ("Press C to return to map")

    while True:
        if keyboard.is_pressed('c'):
            return 
