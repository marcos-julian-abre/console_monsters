import keyboard
import os
from routes import route
import time
from world_map_objects import world_map_object
from pokemon import pokemon
import random
from system_combat import display_combat
import pdb
import state
from system_interactions import display_interactions, display_pc, display_item
import importlib


current_route = "01"
section = 0
route_index = 0
starting_position = route[route_index]['starting_position']

# Design your own map
def get_route(current_route, route) :
    for load_map in route :
        if current_route == load_map['route'] :
            map_route = load_map['route']
            map_layout = load_map['layout']
    
    for index, obj in enumerate(route):
        if obj['route'] == current_route:
            route_index = index

    return map_route, map_layout, route_index

def display_map(player_position, game_route, game_map, characters_position, facing_position, items_position):
    os.system("cls" if os.name == "nt" else "clear")  # Clear the console screen   

    print(section)
    print(game_route)
    print(player_position)
    print(facing_position)
    check_char = 0 
    check_item = 0    

    for row_index, row in enumerate(game_map):
        for col_index, cell in enumerate(row):
            for character in characters_position :
                if (row_index, col_index) == character['position'] :
                    print("C", end=" ")  
                    check_char = 1
            for item in items_position :
                 if (row_index, col_index) == item['position'] :
                     print("O", end=" ")  
                     check_item = 1
            if (row_index, col_index) == player_position:
                print("P", end=" ")  # Display the player character
            elif check_char == 0 and check_item == 0 :
                print(cell, end=" ")
            check_char = 0
            check_item = 0  
            
        print()  # Move to the next line after each row

    print ("Z -- Interact")


def move_player(direction, player_position, facing_position):
    # Update player position based on the direction
    x, y = player_position
    facing_position = player_position
    if direction == "UP":
        player_position = (x - 1, y)
        facing_position = player_position[0] - 1, player_position[1]
    elif direction == "DOWN":
        player_position = (x + 1, y)
        facing_position = player_position[0] + 1, player_position[1]
    elif direction == "LEFT":
        player_position = (x, y - 1)
        facing_position = player_position[0], player_position[1] - 1
    elif direction == "RIGHT":
        player_position = (x, y + 1)
        facing_position = player_position[0], player_position[1] + 1
    return player_position, facing_position


# Example player starting position
player_position = (1,1)
facing_position = (2,1)
last_position = player_position
characters_position = []
items_position = []

for positions in route[route_index]["character"] :
    characters_position.append(positions)
    importlib.reload(state)

for items in route[route_index]["items"] :
    if state.items[0][items["id"]] == True :
        items_position.append(items)    

# Display the initial map with the player
display_map(player_position, current_route, route[0]['layout'], characters_position, facing_position, items_position)


def get_object_type(symbol, world_map_object):
    for obj in world_map_object:
        if obj['key'] == symbol:
            return obj['type']
        
def get_object_section(symbol, world_map_object):
    for obj in world_map_object:
        if obj['key'] == symbol:
            return obj['section']
        
        

def get_encounter(route, section, route_index):
    sum_rarity = 0
    encounters = []    

    for obj in route[route_index]['sections'] :
        if (obj['section'] == section) :
            for pokemon in obj["wild"] :            
                encounter_info = (pokemon['name'], sum_rarity + 1, pokemon['rarity'] + sum_rarity, pokemon['max_level'], pokemon['min_level'])
                encounters.append(encounter_info)
                sum_rarity += pokemon['rarity'] 

                
    random_encounter = random.randint(0,sum_rarity)
    for obj in encounters :
        if (random_encounter > obj[1] and random_encounter < obj[2]) :
            random_level = random.randint(obj[4],obj[3])
            encounter_pokemon = obj[0]
            encounter_level =  random_level

            return (encounter_pokemon, encounter_level)
    
 
def get_characters(route_index, route) :
    characters_position = []
    for positions in route[route_index]["character"] :
        characters_position.append(positions)
    return characters_position


def get_interaction(facing_position, characters_position) :
    for character in characters_position :
        if facing_position == character['position'] :            
            display_interactions(character)
    return 

def get_pc(facing_position, map_layout) : 
    for row_index, row in enumerate(map_layout):
        for col_index, cell in enumerate(row):
            if (row_index, col_index) == facing_position :
                if cell == "$" :
                    display_pc()        
    return

def get_obstacle(facing_position, map_layout) :     
    if state.cut == True :
        for row_index, row in enumerate(map_layout):
            for col_index, cell in enumerate(row):
                if (row_index, col_index) == facing_position :
                    if cell == "!" :   
                        map_layout[row_index][col_index] = "."
    if state.rock_smash == True :
        for row_index, row in enumerate(map_layout):
            for col_index, cell in enumerate(row):
                if (row_index, col_index) == facing_position :
                    if cell == "^":   
                        map_layout[row_index][col_index] = "."
    return map_layout


def get_items(route_index, route) :
    items_position = []
    importlib.reload(state)
    for items in route[route_index]["items"] :
        if state.items[0][items['id']] == True :
            items_position.append(items)
    return items_position


def get_map_item(facing_position, items_position) :
    for item in items_position :
        if facing_position == item['position'] :            
            display_item(item)
    return 


 #UPDATE WHEN ADDING TEAM FUNCTIONALITY   
def check_surf():
    importlib.reload(state)
    if state.surf == True :
        return True
    else :
        return False     

       
    

def map_logic(custom_map,move_position,last_position, route, section, map_route, route_index, characters_position, facing_position, items_position):  
    square = get_object_type(custom_map[move_position[0]][move_position[1]], world_map_object)
    if(square == 'wall') :
        player_position = last_position
        facing_position = move_position
    elif(square == 'terrain'):
        check_char = 0
        check_item = 0
        for characters in characters_position :            
            if (move_position == characters['position']) :  
                player_position = last_position                
                facing_position = move_position               
                check_char = 1
        for items in items_position :
            if (move_position == items['position']) :
                player_position = last_position                
                facing_position = move_position               
                check_item = 1
        if check_char == 0 and check_item == 0:
            player_position = move_position
            last_position = player_position            
    elif(square == 'wild'):
        player_position = move_position
        last_position = player_position
        encounter = random.randint(1, 20)
        if(encounter <= route[route_index]['rate']) :
            encounter_pokemon, encounter_level = get_encounter(route, section, route_index)
            display_combat(world_map_object, player_position, pokemon, route, section, encounter_pokemon, encounter_level)
    elif(square == "section") :
        player_position = move_position        
        last_position = player_position
        section = get_object_section(custom_map[move_position[0]][move_position[1]], world_map_object)
    elif(square == "transport") :
        for exit in route[route_index]['exit'] :
            if exit['section'] == section :
                map_route = exit['destiny']
                for position in route:
                    if position['route'] == exit['destiny'] :
                        for destiny_route in route :
                            if destiny_route["route"] == map_route :                            
                                for come_from in destiny_route['starting_position'] :
                                    if come_from["from"] == route[route_index]['route'] :
                                        player_position = come_from["position"]
                                        section = 0 
                                        facing_position = []                                       
    elif(square == "slope") :
        if (move_position[0] > last_position[0]) :
            jump_position =  move_position[0] + 1, move_position[1]
            jump_facing = facing_position[0] + 1, facing_position[1] 
            player_position = jump_position      
            last_position = player_position
            facing_position = jump_facing
        else : 
            player_position = last_position
            facing_position = move_position
    elif(square == "water") :
        if check_surf() :
            player_position = move_position
            last_position = player_position
        else :
            player_position = last_position 
            facing_position = move_position 
    elif(square == "pc") :
        player_position = last_position
        facing_position = move_position
    elif(square == "obstacle") :
        player_position = last_position
        facing_position = move_position

        
    return (player_position, last_position, section, map_route, facing_position)



# Allow the player to move with directional keys until they choose to exit
while True:
    if keyboard.is_pressed('up'):
        move_position, facing_position = move_player("UP", player_position, facing_position)
    elif keyboard.is_pressed('down'):
        move_position, facing_position = move_player("DOWN", player_position, facing_position)
    elif keyboard.is_pressed('left'):
        move_position, facing_position = move_player("LEFT", player_position, facing_position)
    elif keyboard.is_pressed('right'):
        move_position, facing_position = move_player("RIGHT", player_position, facing_position)    
    if any(keyboard.is_pressed(key) for key in ['up', 'down', 'left', 'right','z']):
        map_route, map_layout, route_index = get_route(current_route, route)
        player_position, last_position, section, current_route, facing_position = map_logic(map_layout, move_position, last_position, route, section, map_route, route_index, characters_position, facing_position, items_position)  
        map_route, map_layout, route_index = get_route(current_route, route)  
        characters_position = get_characters(route_index, route)     
        items_position = get_items(route_index, route) 
    if any(keyboard.is_pressed(key) for key in ['up', 'down', 'left', 'right']):
        display_map(player_position, map_route, map_layout, characters_position, facing_position, items_position) 
    elif keyboard.is_pressed('z'): 
        importlib.reload(state)
        get_interaction(facing_position, characters_position) #UPDATE WHEN BAG IS IMPLEMENTED
        get_pc(facing_position, map_layout) #UPDATE WHEN PC IS IMPLEMENTED
        get_map_item(facing_position, items_position) #UPDATE WHEN BAG IS IMPLEMENTED
        map_layout = get_obstacle(facing_position, map_layout)
        items_position = get_items(route_index, route) 
        display_map(player_position, map_route, map_layout, characters_position, facing_position, items_position) 
    time.sleep(0.1)

