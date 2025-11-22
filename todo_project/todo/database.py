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