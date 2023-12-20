import keyboard
import os
import pdb
import state
import ast
import astunparse
import time
from characters import character as character_data
from interactables import interactable as interactable_data
from  visuals import name_frame, message_frame
from items import item as item_data



def display_interactions(character) :
    os.system("cls" if os.name == "nt" else "clear")  # Clear the console screen    
    i = 0
    number_entries = - 1

    for char in character_data :
        if char["char"] == character["char"] :
            sprite = char["sprite"] 

    name_frame(character["name"])    
    print(sprite)
    message_frame(character["message"][i]["entry"])
    print()
    print ("Press C to continue.")

    for entries in character["message"] :
        number_entries = number_entries + 1

    i = 1
    if i <= number_entries :        
        while True :
            if keyboard.is_pressed('c'): 
                os.system("cls" if os.name == "nt" else "clear")  # Clear the console screen      
                name_frame(character["name"])    
                print(sprite)
                message_frame(character["message"][i]["entry"])
                print()
                print ("Press C to continue.")
                while True :
                    if keyboard.is_pressed('c'):   
                        i = 2          
                        if i <= number_entries :
                            os.system("cls" if os.name == "nt" else "clear")  # Clear the console screen    
                            name_frame(character["name"])    
                            print(sprite)
                            message_frame(character["message"][i]["entry"])
                            print()
                            print ("Press C to continue.")
                            while True :
                                if keyboard.is_pressed('c'): 
                                    i = 3
                                    if i <= number_entries :
                                        os.system("cls" if os.name == "nt" else "clear")  # Clear the console screen    
                                        name_frame(character["name"])    
                                        print(sprite)
                                        message_frame(character["message"][i]["entry"])
                                        print()
                                        print ("Press C to continue.")
                                        
                                    else :
                                        return
                                time.sleep(0.2) 
                        else :
                            return
                    time.sleep(0.2)                             
            time.sleep(0.2)             
    else : 
        while True :
            if keyboard.is_pressed('c'):   
                return
      

        
def display_interactable(interactable):
    os.system("cls" if os.name == "nt" else "clear")  # Clear the console screen    
    i = 0
    number_entries = - 1

    for inter in interactable_data :
        if inter["type"] == interactable["type"] :
            sprite = inter["sprite"] 

    print(sprite)
    message_frame(interactable["message"][i]["entry"])
    print()
    print ("Press C to continue.")


    for entries in interactable["message"] :
        number_entries = number_entries + 1

    i = 1
    if i <= number_entries :        
        while True :
            if keyboard.is_pressed('c'): 
                os.system("cls" if os.name == "nt" else "clear")  # Clear the console screen  
                print(sprite)
                message_frame(interactable["message"][i]["entry"])
                print()
                print ("Press C to continue.")
                while True :
                    if keyboard.is_pressed('c'):   
                        i = 2          
                        if i <= number_entries :
                            os.system("cls" if os.name == "nt" else "clear")  # Clear the console screen  
                            print(sprite)
                            message_frame(interactable["message"][i]["entry"])
                            print()
                            print ("Press C to continue.")
                            while True :
                                if keyboard.is_pressed('c'): 
                                    i = 3
                                    if i <= number_entries :
                                        os.system("cls" if os.name == "nt" else "clear")  # Clear the console screen   
                                        print(sprite)
                                        message_frame(interactable["message"][i]["entry"])
                                        print()
                                        print ("Press C to continue.")                                        
                                    else :
                                        return
                        else :
                            return     
    else : 
        while True :
            if keyboard.is_pressed('c'):   
                return



def display_pc() :
    os.system("cls" if os.name == "nt" else "clear")  # Clear the console screen
    
    print("PC")

    print ("Press C to return to map")

    while True:
        if keyboard.is_pressed('c'):        
            return   
        

def display_item(item) :
    os.system("cls" if os.name == "nt" else "clear")  # Clear the console screen
    
    for items in item_data :
        if items["name"] == item["name"] :
            new_item = items["sprite"]
    
    name_frame(item["name"])
    print(new_item["sprite"])   
    message_frame(item["description"])
    print ("Press C to return to map")

    update_state(item["id"] - 1, False, "items")   

    while True:
        if keyboard.is_pressed('c'):        
            return   
        time.sleep(0.2)
        


def display_engage(trainer) :
    os.system("cls" if os.name == "nt" else "clear")  # Clear the console screen
    
    print(trainer["name"])
    print(trainer["message"])
    print(trainer["sprite"])

    print ("Press C to return to map")

    update_state(trainer["id"] - 1, False, 'trainers')   

    while True:
        if keyboard.is_pressed('c'):        
            return 
        time.sleep(0.2)
        



def update_state(item_index, new_state, update_type):

    state_file_path = os.path.join(os.path.dirname(__file__), 'state.py')

    # Read the content of state.py
    with open(state_file_path, 'r') as file:
        content = file.read()

    try:
        # Parse the content into an abstract syntax tree (AST)
        tree = ast.parse(content, filename=state_file_path)

        # Find the 'items' dictionary node
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and node.targets[0].id == update_type:
                # Update the item in the dictionary within the list
                node.value.elts[0].values[item_index] = ast.Constant(value=new_state)

        # Convert the AST back to a string
        updated_content = astunparse.unparse(tree)
    except Exception as e:
        print(f"Error during AST manipulation: {e}")
        return

    # Write the updated content back to state.py
    with open(state_file_path, 'w') as file:
        file.write(updated_content)


    return

