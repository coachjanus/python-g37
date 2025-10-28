'''

'''
import sys, os
import argparse
from pathlib import Path
from . import ui
from .db import create_db

def main(db_name):
    ui.hi()
    create_db(db_name)

    while True:
        match ui.your_choice():
            case 'a':
                ui.add_contact(db_name)
            case 'l':
                ui.contact_list(db_name)
            case 'u':
                ui.edit_contact(db_name)
               
            case 'd':
                ui.remove_contact(db_name)
                
            case 'h':
                ui.help_me()
            case 'q':
                ui.bye()
                break
            case _:
                ui.help_me()
         

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="phone book", description="List of my contacts" , epilog="Thanks for using %(prog)s! :)"
    )
    
    general = parser.add_argument_group('general output')
    general.add_argument(
        "path",
        nargs="?",
        default="db.pkl",
        help="Take the path to the target database file (default: %(default)s)"
    )
    
    args = parser.parse_args()
    
    execute_dir = os.getcwd()
    file_dir = os.path.dirname(os.path.realpath(__file__))
    
    db_name = Path(os.path.relpath(file_dir/Path(args.path)))
    
    main(db_name)