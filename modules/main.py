'''

'''
import sys
import ui
from db import create_db

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
    if (args_cont := len(sys.argv)) > 2:
        print(f"One argument expected, got {args_cont -1}")
        raise SystemExit(1)
    elif args_cont < 2:
        print(f"You must specify the database name")
        raise SystemExit(1)
    db_name = sys.argv[1]
    main(db_name)