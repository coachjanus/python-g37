"""_summary_"""

import pickle

contacts = []

TITLE = "phone book"

def save_contact(contacts):
    with open('db.pkl', 'wb') as f:
        pickle.dump(contacts, f)

# contact = {
#     'first_name': 'john',
#     'last_name': 'doe',
#     'mobile': '1234567'
# }

# contacts.append(contact)
# save_contact(contacts)


def contact_list(contacts):
    if len(contacts) > 0:
        for item in contacts:
            for k,v in item.items():
                print(k, ' => ', v) 
    else:
        print("Your contact list is empty. Go back to menu and add new contact.")


def your_choice():
    return input(f"Please make Your choice (l|a|u|d|h|q) >>> ")

def add_contact():
    contact = {}
    first_name = input("Enter firstr name: ").strip().lower()
    last_name = input("Enter last name: ").strip().lower()
    mobile = input("Enter phoner phone number: ").strip()
    contact['first_name'] = first_name
    contact['last_name'] = last_name
    contact['mobile'] = mobile
    return contact

def help_me():
    print("""
    All that You can do:
        l: List existing contacts
        a: Add new contact
        u: Edit existing contact
        d: Delete existing contact
        h: Print this help
        q: Exit
    """)

def bye():
    print(f"Thanks for using {TITLE}")
    
def hi():
    print(f"Hi! It's me, {TITLE.upper()}")
    
def remove_contact(contact):
    index = contacts.index(contact)
    confirm = input("Are You sure You want delete this contact? (y/n): ").strip()
    if confirm.lower() in ('yes', 'y'):
        return contacts.pop(index)
    return
    
def lookup_contact(name):
    first_name = ''
    last_name = ''
    
    words = name.split()
    
    if len(words) == 2:
        first_name, last_name = words
    elif len(words) == 1:
        first_name = words[0]
        
    for d in contacts:
        if d['first_name'] == first_name.lower() and d['last_name'] == last_name.lower():
            return d
        elif d['first_name'] == words[0].lower() or d['last_name'] == words[0].lower():
            return d

def update_contact(contact):
    old_first_name = contact['first_name']
    old_last_name = contact['last_name']
    old_mobile = contact['mobile']
    first_name = input(f"Enter first name: ({old_first_name}) >>> ").strip().lower() or old_first_name
    last_name = input(f"Enter last name: ({old_last_name}) >>> ").strip().lower() or old_last_name
    mobile = input(f"Enter phone number: ({old_mobile}) >>> ").strip() or old_mobile
    
    return {'first_name': first_name.lower(), 'last_name': last_name.lower(), 'mobile': mobile}

def load_contact(db_name):
    unpiclled = []
    # with open('db.pkl', 'rb') as f:
    with open(db_name, 'rb') as f:
        unpiclled = pickle.load(f)
    return unpiclled

def main(db_name):
    hi()
    contacts = load_contact(db_name)
    
    while True:
        match your_choice():
            case 'a':
                contacts.append(add_contact())
                save_contact(contacts)
            case 'l':
                contact_list(contacts)
            case 'u':
                name = input("What You looking for? ")
                contact = lookup_contact(name)
                contact.update(update_contact(contact))
                save_contact(contacts)
            case 'd':
                name = input("What You looking for? ")
                contact = lookup_contact(name)
                contact = remove_contact(contact)
                if contact:
                    print("Contact removed successfuly.")
                    save_contact(contacts)
            case 'h':
                help_me()
            case 'q':
                bye()
                break
            case _:
                help_me()
         
import sys

# print(sys.argv)
# print(sys.argv[1])

# print(db_name)

if (args_cont := len(sys.argv)) > 2:
    print(f"One argument expected, got {args_cont -1}")
    raise SystemExit(1)
elif args_cont < 2:
    print(f"You must specify the database name")
    raise SystemExit(1)

db_name = sys.argv[1]
main(db_name)            
