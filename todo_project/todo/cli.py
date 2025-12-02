
"""
This module contains the main application function for the todo CLI.
It uses the Typer library to create a command-line interface (CLI) for managing todo tasks.
Initialize the todo CLI application.
Creates the application configuration file and initializes the todo database
at the specified path. If either the config file creation or database initialization
fails, displays an error message and exits with status code 1.
Functions:
    init(db_path: str) -> None:
        Initializes the todo application by creating the configuration file
        and initializing the database at the specified path.
    run() -> None:
        Runs the main loop of the todo CLI application, allowing users to
        interactively manage their todo tasks.

Args:
    db_path: The file path where the todo database will be created or stored.
            Defaults to the DEFAULT_DB_FILE_PATH from config. Can be overridden
            via the --db-path or -db command-line option.
Raises:
    typer.Exit: Exits with code 1 if config file creation or database initialization fails.
"""

from todo.ui import UI
import typer
from todo import config, ERRORS, database as db
from pathlib import Path
from typing import Annotated
import logging

app = typer.Typer()

# logging.basicConfig(format="%(levelname)s:%(name)s:%(message)s")
# logging.warning("Hello, Warning!")
# logging.basicConfig(format="{levelname}:{name}:{message}", style="{")
# logging.basicConfig(
#     format="{asctime} - {levelname} - {message}",
#     style="{",
#     datefmt="%Y-%m-%d %H:%M",
# )
# logging.error("Something went wrong!")

# logging.basicConfig(
#     filename="app.log",
#     encoding="utf-8",
#     filemode="a",
#     format="{asctime} - {levelname} - {message}",
#     style="{",
#     datefmt="%Y-%m-%d %H:%M",
#     level=logging.DEBUG,)
# logging.warning("Save me!")

# logging.basicConfig(
#     format="{asctime} - {levelname} - {message}",
#     style="{",
#     datefmt="%Y-%m-%d %H:%M",
#     level=logging.DEBUG,
# )
# name = "Samsara"
# logging.debug(f"{name=}")
# # 2025-11-22 14:49 - DEBUG - name='Samsara'

# logging.basicConfig(
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     style="%",
#     datefmt="%Y-%m-%d %H:%M",
#     level=logging.DEBUG,
# )
# name = "Samsara"
# logging.debug("name=%s", name)

# import logging
# logger = logging.getLogger(__name__)
# console_handler = logging.StreamHandler()
# file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")

# logger.addHandler(console_handler)
# logger.addHandler(file_handler)
# logger.handlers
# # [
# #   <StreamHandler <stderr> (NOTSET)>,
# #   <FileHandler /home/janus/app.log (NOTSET)>
# # ]

# logger = logging.getLogger(__name__)
# console_handler = logging.StreamHandler()
# file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
# logger.addHandler(console_handler)
# logger.addHandler(file_handler)
# formatter = logging.Formatter(
#    "{asctime} - {levelname} - {message}",
#     style="{",
#     datefmt="%Y-%m-%d %H:%M",
# )
# console_handler.setFormatter(formatter)
# logger.warning("Stay calm!")

# logger = logging.getLogger(__name__)
# logger.level
# # 0

# logger
# # <Logger __main__ (WARNING)>

# logger.parent
# # <RootLogger root (WARNING)>

# formatter = logging.Formatter("{levelname} - {message}", style="{")
# console_handler = logging.StreamHandler()
# console_handler.setFormatter(formatter)
# logger.addHandler(console_handler)
# logger.debug("Just checking in!")
# logger.info("Just checking in, again!")
# # INFO - Just checking in, again!

# console_handler.setLevel("DEBUG")
# logger.debug("Just checking in!")
# console_handler
# # <StreamHandler <stderr> (DEBUG)>

# logger = logging.getLogger(__name__)
# logger.setLevel("DEBUG")
# formatter = logging.Formatter("{levelname} - {message}", style="{")

# console_handler = logging.StreamHandler()
# console_handler.setLevel("DEBUG")
# console_handler.setFormatter(formatter)
# logger.addHandler(console_handler)

# file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
# file_handler.setLevel("WARNING")
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

# logger.debug("Just checking in!")
# # DEBUG - Just checking in!

# logger.warning("Stay curious!")
# # WARNING - Stay curious!

# logger.error("Stay put!")
# # ERROR - Stay put!


# def show_only_debug(record):
#     return record.levelname == "DEBUG"

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")
formatter = logging.Formatter(
   "{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)
# formatter = logging.Formatter("{levelname} - {message}", style="{")

# console_handler = logging.StreamHandler()
# console_handler.setLevel("DEBUG")
# console_handler.setFormatter(formatter)
# console_handler.addFilter(show_only_debug)
# logger.addHandler(console_handler)

file_handler = logging.FileHandler("todo.log", mode="a", encoding="utf-8")
file_handler.setLevel("DEBUG")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# logger.debug("Just checking in!")
# # DEBUG - Just checking in!

# logger.warning("Stay curious!")
# logger.error("Stay put!")


@app.command()
def init(
    db_path: Annotated[str, typer.Option("--db-path", "-db", prompt="TODO database location?"), ] = str(config.DEFAULT_DB_FILE_PATH), ) -> None:
    
    """Initialize the todo CLI application."""
    
    app_init_error = config.init_app(db_path)
    
    if app_init_error:
        typer.secho(f"Crerating config file failed with {ERRORS[app_init_error]}", fg=typer.colors.RED)
        logger.error(f"Crerating config file failed with {ERRORS[app_init_error]}")
        raise typer.Exit(1)
    
    db_init_error = db.init_database(Path(db_path))
    if db_init_error:
        typer.secho(f"Crerating database failed with {ERRORS[db_init_error]}", fg=typer.colors.RED)
        logger.error(f"Crerating database failed with {ERRORS[db_init_error]}")
        raise typer.Exit(1)
    
    typer.secho(f"The todo database is {db_path}", fg=typer.colors.GREEN)
    logger.info(f"The todo database is {db_path}")



"""
Run the todo CLI application main loop.
Initializes the UI and enters an interactive loop that processes user commands:
- 'a': Add a new todo task
- 'l': List all tasks
- 'u': Mark a task as done
- 'd': Delete a task
- 'h': Display help information
- 'q': Quit the application
Any unrecognized input displays the help menu. The loop continues until
the user selects 'q' to quit.
"""

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

