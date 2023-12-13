import keyboard
import os
import pdb




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

    while True:
        if keyboard.is_pressed('c'):        
            return   
        