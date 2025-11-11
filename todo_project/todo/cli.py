'''
This module contains the main application function for the todo CLI.
'''
from todo.ui import UI

def app():
    # print("This is the main application function." )
    ui = UI()
    
    ui.display_message("Welcome to the Todo Application!")

    print( "UI class initialized with the following settings:" )
    print( f"Status Symbols:" )
    print( f"✓ Done: {ui.DONE} ")
    print( f"○ Pending: {ui.PENDING} ")
    print( f"COLORS: {ui.COLORS} ")
    # print( f"HEADERS: {ui.HEADERS} ")