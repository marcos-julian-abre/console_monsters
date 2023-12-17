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
from system_interactions import display_interactions, display_pc, display_item, display_engage, display_interactable
import importlib



current_route = "PAL"
section = 0
route_index = 0
starting_position = route[route_index]['starting_position']


def display_map(player_position, game_route, game_map, characters_position, facing_position, items_position, trainers_position):
    os.system("cls" if os.name == "nt" else "clear")  # Clear the console screen   

    print(section)
    print(game_route)
    print(player_position)
    print(facing_position)
    print(characters_position)
    check_char = 0 
    check_item = 0    

    for row_index, row in enumerate(game_map):
        for col_index, cell in enumerate(row):
            for character in characters_position :
                if (row_index, col_index) == character['position'] :
                    print("C", end=" ")  
                    check_char = 1
            for trainer in trainers_position :
                if (row_index, col_index) == trainer['position'] :
                    print("T", end=" ")  
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
player_position = (7,11)
facing_position = (8,11)
last_position = player_position
characters_position = []
trainers_position = []
items_position = []
interactables_position = []

for positions in route[route_index]["character"] :
    characters_position.append(positions)    

for positions in route[route_index]["trainer"] :
   trainers_position.append(positions)

for items in route[route_index]["items"] :
    if state.items[0][items["id"]] == True :
        items_position.append(items)  

for interactables in route[route_index]["interactables"] :
    interactables_position.append(interactables)  

# Display the initial map with the player
display_map(player_position, current_route, route[0]['layout'], characters_position, facing_position, items_position, trainers_position)



def get_object_type(symbol, world_map_object):
    for obj in world_map_object:
        if obj['key'] == symbol:
            return obj['type']
        

        
def get_object_section(symbol, world_map_object):
    for obj in world_map_object:
        if obj['key'] == symbol:
            return obj['section']
        

        
def get_route(current_route, route) :
    for load_map in route :
        if current_route == load_map['route'] :
            map_route = load_map['route']
            map_layout = load_map['layout']
    
    for index, obj in enumerate(route):
        if obj['route'] == current_route:
            route_index = index

    return map_route, map_layout, route_index        



def get_encounter(route, section, route_index):
    sum_rarity = -1
    encounters = []  

    for sec in route[route_index]['catch'] :
        if (sec['section'] == section) :
            for pokemon in sec["wild"] :            
                encounter_info = pokemon
                encounter_info["sum_rarity"] = sum_rarity + 1                
                sum_rarity += pokemon['rarity'] 
                encounter_info["rarity"] = sum_rarity 
                encounters.append(encounter_info)

                
    random_encounter = random.randint(1,sum_rarity)
    for pokemon in encounters :
        if (random_encounter > pokemon["sum_rarity"] and random_encounter < pokemon["rarity"]) :
            random_level = random.randint(pokemon["level"]["min"],pokemon["level"]["max"])
            encounter_pokemon = pokemon["name"]
            encounter_level =  random_level

            return (encounter_pokemon, encounter_level)



def get_engage(player_position, facing_position, trainers_position, moving) : #UPDATE WHEN COMBAT IS IMPLEMENTED
    importlib.reload(state)    
    if moving == True :
        for trainer in trainers_position :
            if state.trainers[0][trainer["id"]] == True :
                for pattern in trainer["pattern"] :
                    for position in pattern["facing_position"] :
                        for facing in position[trainer["patrol"]] :
                            if facing['face'] == player_position :
                                display_engage(trainer) 
    if moving == False :
        for trainer in trainers_position :
            if state.trainers[0][trainer["id"]] == True :
                if trainer["position"] == facing_position :
                    display_engage(trainer)
    return
            


def get_interactables(current_route, route) :
    trash1, trash2, route_index = get_route(current_route, route)
    
    for interactables in route[route_index]["interactables"] :
        interactables_position.append(interactables)  
    return interactables_position
    

 
def get_characters(route_index, route, past_characters_position, player_position) :
    characters_position = []
    character = []
    check_route = 0    
    check_pattern = 0

    for characters in route[route_index]["character"] :
        for past_characters in past_characters_position :
            if past_characters['name'] == characters["name"] :
                check_route = 1    

    for characters in route[route_index]["character"] :
        if characters["type"] == "standing" :
            characters_position.append(characters)             
        if characters["type"] == "patrol" :
            if check_route == 0 :
                characters_position.append(characters)

    if check_route == 1 :
        for past_position in past_characters_position :
            if past_position["type"] == "patrol" :
                if check_pattern == 1 :
                    break
                elif past_position["patrol"] == 0 :
                    for pattern in past_position["pattern"] :
                        if pattern["starting_position"] == past_position["position"] :
                            if pattern["going_position"] == True :
                                character = past_position
                                character["patrol"] = 1
                                characters_position.append(character)
                                check_pattern = 1
                                break
                            else :
                                if pattern["going_position"] != player_position :
                                    character = past_position
                                    character['position'] = pattern["going_position"]
                                    characters_position.append(character)
                                    check_pattern = 1
                                    break
                                else :
                                    character = past_position
                                    characters_position.append(character)
                                    check_pattern = 1
                                    break
                elif past_position["patrol"] == 1 :
                    for pattern in past_position["pattern"] :
                        if pattern["starting_position"] == past_position["position"] :
                            if pattern["coming_position"] == True :
                                character = past_position
                                character["patrol"] = 0
                                characters_position.append(character)
                                check_pattern = 1
                                break
                            else :
                                if pattern["coming_position"] != player_position : 
                                    character = past_position
                                    character['position'] = pattern["coming_position"]
                                    characters_position.append(character)
                                    check_pattern = 1
                                    break
                                else :
                                    character = past_position
                                    characters_position.append(character)
                                    check_pattern = 1
                                    break
    
    return characters_position



def get_trainers(route_index, route, past_trainers_position, player_position) :
    trainers_position = []
    trainer = []
    check_route = 0    
    check_pattern = 0

    for trainers in route[route_index]["trainer"] :
        for past_trainers in past_trainers_position :
            if past_trainers['name'] == trainers["name"] :
                check_route = 1    

    for trainers in route[route_index]["trainer"] :
        if trainers["type"] == "standing" :
            trainers_position.append(trainers)             
        if trainers["type"] == "patrol" :
            if check_route == 0 :
                trainers_position.append(trainers)

    if check_route == 1 :
        for past_position in past_trainers_position :
            if past_position["type"] == "patrol" :
                if check_pattern == 1 :
                    break
                elif past_position["patrol"] == 0 :
                    for pattern in past_position["pattern"] :
                        if pattern["starting_position"] == past_position["position"] :
                            if pattern["going_position"] == True :
                                trainer = past_position
                                trainer["patrol"] = 1
                                trainers_position.append(trainer)
                                check_pattern = 1
                                break
                            else :
                                if pattern["going_position"] != player_position :
                                    trainer = past_position
                                    trainer['position'] = pattern["going_position"]
                                    trainers_position.append(trainer)
                                    check_pattern = 1
                                    break
                                else :
                                    trainer = past_position
                                    trainers_position.append(trainer)
                                    check_pattern = 1
                                    break
                elif past_position["patrol"] == 1 :
                    for pattern in past_position["pattern"] :
                        if pattern["starting_position"] == past_position["position"] :
                            if pattern["coming_position"] == True :
                                trainer = past_position
                                trainer["patrol"] = 0
                                trainers_position.append(trainer)
                                check_pattern = 1
                                break
                            else :
                                if pattern["coming_position"] != player_position : 
                                    trainer = past_position
                                    trainer['position'] = pattern["coming_position"]
                                    trainers_position.append(trainer)
                                    check_pattern = 1
                                    break
                                else :
                                    trainer = past_position
                                    trainers_position.append(trainer)
                                    check_pattern = 1
                                    break
    
    return trainers_position



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



def get_read(facing_position, interactables_position) :
    for interactable in interactables_position :
        if facing_position == interactable["position"] : 
            display_interactable(interactable)
    return


 #UPDATE WHEN ADDING TEAM FUNCTIONALITY   
def check_surf():
    importlib.reload(state)
    if state.surf == True :
        return True
    else :
        return False     

       
    
def map_logic(custom_map,move_position,last_position, route, section, map_route, route_index, characters_position, facing_position, items_position, trainers_position, interactables_position):  
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
        for trainers in trainers_position :            
            if (move_position == trainers['position']) :  
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

    elif(square == 'wild'): #UPDATE WHEN CATCH IS IMPLEMENTED
        rate = 0
        check_char = 0
        check_item = 0
        for characters in characters_position :            
            if (move_position == characters['position']) :  
                player_position = last_position                
                facing_position = move_position               
                check_char = 1
        for trainers in trainers_position :            
            if (move_position == trainers['position']) :  
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
        encounter = random.randint(1, 100)
        for sec in route[route_index]['catch'] :
            if sec["section"] == section :
                rate = sec["rate"]
        if(encounter <= rate) :   
            encounter_pokemon, encounter_level = get_encounter(route, section, route_index)
            display_combat(encounter_pokemon, encounter_level)

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
        interactables_position = get_interactables(map_route, route)                 

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


    return (player_position, last_position, section, map_route, facing_position, interactables_position)



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
        player_position, last_position, section, current_route, facing_position, interactables_position = map_logic(map_layout, move_position, last_position, route, section, map_route, route_index, characters_position, facing_position, items_position, trainers_position, interactables_position)  
        map_route, map_layout, route_index = get_route(current_route, route)  
        characters_position = get_characters(route_index, route, characters_position, player_position) 
        trainers_position = get_trainers(route_index, route, trainers_position, player_position)    
        items_position = get_items(route_index, route) 
    if any(keyboard.is_pressed(key) for key in ['up', 'down', 'left', 'right']):
        get_engage(player_position, facing_position, trainers_position, moving = True)      
        display_map(player_position, map_route, map_layout, characters_position, facing_position, items_position, trainers_position) 
    if any(keyboard.is_pressed(key) for key in ['c']):
        display_map(player_position, map_route, map_layout, characters_position, facing_position, items_position, trainers_position) 
    elif keyboard.is_pressed('z'): 
        importlib.reload(state)
        get_interaction(facing_position, characters_position) #UPDATE WHEN BAG IS IMPLEMENTED'
        get_pc(facing_position, map_layout) #UPDATE WHEN PC IS IMPLEMENTED
        get_map_item(facing_position, items_position) #UPDATE WHEN BAG IS IMPLEMENTED
        get_engage(player_position, facing_position, trainers_position, moving = False)#UPDATE WHEN CCOMBAT IS IMPLEMENTED
        get_read(facing_position, interactables_position)
        map_layout = get_obstacle(facing_position, map_layout)
        items_position = get_items(route_index, route) 
        display_map(player_position, map_route, map_layout, characters_position, facing_position, items_position, trainers_position) 
    time.sleep(0.15)

