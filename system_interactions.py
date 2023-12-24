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
from trainers import trainer as trainer_data
import importlib



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
                                time.sleep(0.1) 
                        else :
                            return
                    time.sleep(0.1)                             
            time.sleep(0.1)             
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
            sprite = items["sprite"]
            description = items["description"]
    
    name_frame(item["name"])
    print(sprite)   
    message_frame(description)
    print()
    print ("Press C to return to map")

    try:
        if item["id"] :
            update_state(item["id"] - 1, False, "items")   
    except :
        error = "no id"

    while True:
        if keyboard.is_pressed('c'):        
            return   
        time.sleep(0.15)


        
def display_healing() :
    os.system("cls" if os.name == "nt" else "clear")  # Clear the console screen   

    print("Healing")
    print ("Press C to return to map")

    while True:
        if keyboard.is_pressed('c'):        
            return   
        time.sleep(0.15)



def display_shop() :
    os.system("cls" if os.name == "nt" else "clear")  # Clear the console screen   

    print("Shop")
    print ("Press C to return to map")

    while True:
        if keyboard.is_pressed('c'):        
            return   
        time.sleep(0.15)
        


def display_engage(trainer) :
    os.system("cls" if os.name == "nt" else "clear")  # Clear the console screen
    
    for trainers in trainer_data :
        if trainers["char"] == trainer["char"] : 
            sprite = trainers["sprite"]


    name_frame(trainer["name"])
    print(sprite)        
    if state.trainers[0][trainer["id"]] == True:
        message_frame(trainer["message"][0][0][0]["entry"])
        
    if state.trainers[0][trainer["id"]] == False:
        message_frame(trainer["message"][2][2][0]["entry"])

    print()        

    print ("Press C to return to map")

    update_state(trainer["id"] - 1, False, 'trainers')   

    while True:
        if keyboard.is_pressed('c'):        
            return 
        time.sleep(0.15)
        



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

def display_menu():
    os.system("cls" if os.name == "nt" else "clear")  # Clear the console screen   

    print ("B -- Bag")    
    print ("C -- Return")


    while True :
        if keyboard.is_pressed('c'):   
            return
        if keyboard.is_pressed('b') :
            display_bag()



def display_bag():
    os.system("cls" if os.name == "nt" else "clear")  # Clear the console screen       
    importlib.reload(state)
    inventory = state.inventory
    lista_items = []
    i = 0

    try :
        for items in inventory:
            for item_info in item_data:
                if items["name"] == item_info["name"]:
                    item_info["quantity"] = items["quantity"]
                    lista_items.append(item_info)
    except :
        error = "no items"


    while i <= 9 :
        print(str(i) + ". ", end=" ")
        try :
            if lista_items[i] :
                print(lista_items[i]["name"], end=" ")
                print(lista_items[i]["quantity"], end=" ")
        except : 
            error = "not enough items in inventory"
        print()
        i = i + 1


    print()
    print ("C -- Return")
    
    while True :
        if keyboard.is_pressed('c'):   
            return
        try :
            if lista_items[0] : 
                if keyboard.is_pressed('0'):   
                    display_item_menu(0)
        except :
             error = "no item"
        try :
            if lista_items[1] : 
                if keyboard.is_pressed('1'):   
                    display_item_menu(1)
        except :
             error = "no item"
        try :
            if lista_items[2] : 
                if keyboard.is_pressed('2'):   
                    display_item_menu(2)
        except :
             error = "no item"
        try :
            if lista_items[3] : 
                if keyboard.is_pressed('3'):   
                    display_item_menu(3)
        except :
             error = "no item"
        try :
            if lista_items[4] : 
                if keyboard.is_pressed('4'):   
                    display_item_menu(4)
        except :
            error = "no item"
        try :
            if lista_items[5] : 
                if keyboard.is_pressed('5'):   
                    display_item_menu(5)
        except :
            error = "no item"
        try :
            if lista_items[6] : 
                if keyboard.is_pressed('6'):   
                    display_item_menu(6)
        except :
            error = "no item"
        try :
            if lista_items[7] : 
                if keyboard.is_pressed('7'):   
                    display_item_menu(7)
        except :
            error = "no item"
        try :
            if lista_items[8] : 
                if keyboard.is_pressed('8'):   
                    display_item_menu(8)
        except :
            error = "no item"
        try :
            if lista_items[9] : 
                if keyboard.is_pressed('9'):   
                    display_item_menu(9)
        except :
            error = "no item"




def display_item_menu(id):        
    os.system("cls" if os.name == "nt" else "clear")  # Clear the console screen
    importlib.reload(state)
    inventory = state.inventory
    item = []


    for items in item_data:
        if items["name"] == inventory[id]["name"] :
            items["quantity"] = inventory[id]["quantity"]
            item = items

    
    name_frame(item["name"])
    print("   Quantity : " + str(item["quantity"]))   
    message_frame(item["description"])
    print()
    print()


    if item["pocket"] == "medicine":
        print("1 - Use")
        print("2 - Info")       
        print ("C - Cancel")
        
        while True :
            if keyboard.is_pressed('1'):   
                return
            if keyboard.is_pressed('2'): 
                display_item(item)
            if keyboard.is_pressed('c'):   
                return


    if item["pocket"] == "pokeball":
        print("1 - Info")       
        print("C - Cancel")

        while True :
            if keyboard.is_pressed('1'):   
                display_item(item)
            if keyboard.is_pressed('c'):   
                return







