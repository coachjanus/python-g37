'''
This module contains the main application function for the todo CLI.
'''
from todo.ui import UI
import typer
from todo import config, ERRORS, database as db
from pathlib import Path

app = typer.Typer()

@app.command()
def init(
    db_path = typer.Option(
        str(config.DEFAULT_DB_FILE_PATH), 
        prompt="TODO database location?")):
    
    """Initialize the todo CLI application."""
    
    app_init_error = config.init_app(db_path)
    
    if app_init_error:
        typer.secho(f"Crerating config file failed with {ERRORS[app_init_error]}", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    db_init_error = db.init_database(Path(db_path))
    if db_init_error:
        typer.secho(f"Crerating database failed with {ERRORS[db_init_error]}", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    typer.secho(f"The todo database is {db_path}", fg=typer.colors.GREEN)

@app.command()
def run():
    """Run the todo CLI application."""
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

