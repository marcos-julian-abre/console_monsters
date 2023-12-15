import keyboard
import os
import pdb
import state
import ast
import astunparse



def display_interactions(character) :
    os.system("cls" if os.name == "nt" else "clear")  # Clear the console screen
    
    print(character["name"])
    print(character["message"])
    print(character["sprite"])

    print ("Press C to return to map")

    while True:
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
    
    print(item["name"])   
    print ("Press C to return to map")

    update_state(item["id"] - 1, False, "items")   

    while True:
        if keyboard.is_pressed('c'):        
            return   
        


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

