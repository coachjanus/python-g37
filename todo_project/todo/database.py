"""
todo/database.py
This module provides functions for initializing and accessing the todo application's database.
Functions:
    init_database(db_path: Path):
        Initializes the database file at the specified path by writing an empty list ("[]").
        Returns a status code indicating success or a write error.
    get_database_path(config_file):
        Reads the configuration file and returns the path to the database as specified in the "General" section.
"""

import configparser
from pathlib import Path
from todo import SUCCESS, DB_WRITE_ERROR

def init_database(db_path: Path):
    try:
        db_path.write_text("[]")
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR
    
def get_database_path(config_file):
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])