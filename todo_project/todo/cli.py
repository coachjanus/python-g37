'''
This module contains the main application function for the todo CLI.
'''
from todo.ui import UI

def app():
    
    # print("This is the main application function.")
    """Main application entry point for the todo CLI."""
    ui = UI()
    print("Todo CLI Application Initialized")
    print("UI class initialized with the following settings:")
    print(f"Status Symbols:")
    print(f"✓ Done: {ui.DONE}")
    print(f"○ Pending: {ui.PENDING}")
    
    print(f"COLORS: {ui.COLORS}")
    print(f"HEADERS: {ui.HEADERS}")
    
    ui.hi()
    
    while True:
        match ui.your_choice():
            case 'a':
                ui.add_todo()
            case 'l':
                ui.get_all_task()
            case 'u':
                ui.set_done_task()
            case 'd':
                ui.remove_task()
                
            case 'h':
                ui.help_me()
            case 'q':
                ui.bye()
                break
            case _:
                ui.help_me()