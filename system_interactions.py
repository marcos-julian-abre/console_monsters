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
            item_id = items["item_id"]


    for diccionary in state.inventory :
        if item_id in diccionary :
            quantity = diccionary[item_id] + 1

    
    
    name_frame(item["name"])
    print(sprite)   
    message_frame(description)
    print()
    print ("Press C to return to map")

    try:
        if item["id"] :
            update_state(item["id"] - 1, False, "items")               
            update_state(item_id - 1, quantity, "inventory")   

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



def display_shop(shop_route) :
    os.system("cls" if os.name == "nt" else "clear")  # Clear the console screen  
    shop = [] 

    for shop_items in shop_route :
        for items in item_data :
            if shop_items["name"] == item_data["name"] :
                shop_items = items
                shop_items["price"] = items["price"]
                shop.append(shop_items)

    print("Shop")
    
    while i <= 9 :
        try :
            if shop[i] :                
                print(str(i) + ". ", end=" ")
                print(shop[i]["name"], end=" ")
                print(shop[i]["price"], end=" ")
        except : 
            error = "not enough items in inventory"
        print()
        i = i + 1


    print()
    print ("C -- Return")

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


    for items in item_data:
        for dictionary in inventory :
            if items["item_id"] in dictionary :
                items["quantity"] = dictionary[items["item_id"]]
                if items["quantity"] > 0 :
                    lista_items.append(items)            


    print("Bag")    
    print()

    while i <= 9 :
        print(str(i) + ". ", end=" ")
        try :
            if lista_items[i] and lista_items[i]["quantity"] > 0:
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
            if lista_items[0] and lista_items[0]["quantity"] > 0: 
                if keyboard.is_pressed('0'):   
                    display_item_menu(lista_items[0])
        except :
             error = "no item"
        try :
            if lista_items[1] and lista_items[1]["quantity"] > 0: 
                if keyboard.is_pressed('1'):   
                    display_item_menu(lista_items[1])
        except :
             error = "no item"
        try :
            if lista_items[2] and lista_items[2]["quantity"] > 0:
                if keyboard.is_pressed('2'):   
                    display_item_menu(lista_items[2])
        except :
             error = "no item"
        try :
            if lista_items[3] and lista_items[3]["quantity"] > 0: 
                if keyboard.is_pressed('3'):   
                    display_item_menu(lista_items[3])
        except :
             error = "no item"
        try :
            if lista_items[4] and lista_items[4]["quantity"] > 0: 
                if keyboard.is_pressed('4'):   
                    display_item_menu(lista_items[4])
        except :
            error = "no item"
        try :
            if lista_items[5] and lista_items[5]["quantity"] > 0: 
                if keyboard.is_pressed('5'):   
                    display_item_menu(lista_items[5])
        except :
            error = "no item"
        try :
            if lista_items[6] and lista_items[6]["quantity"] > 0: 
                if keyboard.is_pressed('6'):   
                    display_item_menu(lista_items[6])
        except :
            error = "no item"
        try :
            if lista_items[7] and lista_items[7]["quantity"] > 0: 
                if keyboard.is_pressed('7'):   
                    display_item_menu(lista_items[7])
        except :
            error = "no item"
        try :
            if lista_items[8] and lista_items[8]["quantity"] > 0: 
                if keyboard.is_pressed('8'):   
                    display_item_menu(lista_items[8])
        except :
            error = "no item"
        try :
            if lista_items[9] and lista_items[9]["quantity"] > 0: 
                if keyboard.is_pressed('9'):   
                    display_item_menu(lista_items[9])
        except :
            error = "no item"




def display_item_menu(item):        
    os.system("cls" if os.name == "nt" else "clear")  # Clear the console screen
    importlib.reload(state)
    inventory = state.inventory


    name_frame(item["name"])
    print()
    print()


    if item["pocket"] == "medicine":
        print("U - Use")
        print("I - Info")       
        print ("C - Cancel")
        
        while True :
            if keyboard.is_pressed('u'):                  
                importlib.reload(state)
                update_state(item["item_id"] - 1, item["quantity"] - 1, "inventory")        
                print("Item Used. Press C to Return")           
                return               
            if keyboard.is_pressed('i'): 
                display_item(item)
            if keyboard.is_pressed('c'):   
                return


    if item["pocket"] == "pokeball":
        print("I - Info")       
        print("C - Cancel")

        while True :
            if keyboard.is_pressed('i'):   
                display_item(item)
            if keyboard.is_pressed('c'):   
                return







