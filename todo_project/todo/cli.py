'''
This module contains the main application function for the todo CLI.
'''
from todo.ui import UI
import typer

app = typer.Typer()

@app.command()
def init():
    """Initialize the todo CLI application."""
    print("Todo CLI Application Initialized")

@app.command()
def run():
    """Run the todo CLI application."""
    # def app():
    
    # print("This is the main application function.")
    """Main application entry point for the todo CLI."""
    ui = UI()
       
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