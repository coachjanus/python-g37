"""_summary_
"""

import pickle
import sys


TITLE = "Phone book"

contacts = []

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
    print (f"Thanks for using {TITLE}")
    

def hello():
    print (f"Hi! This is {TITLE}")

def contacts_list(contacts):
    if len(contacts) > 0:
        for contact in contacts:   
            print(f"{contacts.index(contact)} Name: {full_name(contact)} Phonew number: {contact['phone_number']} Address: {contact['address']}")    
    else:
        print("Your contact list is empty. Go back to menu and add new contact.")
        
def full_name(contact):
    return contact['first_name'].title() + " " + contact['last_name'].title()

def add_contact():
    
    contact = {}
    contact['first_name'] =  input('Enter Your First Name: ').strip().lower()
    contact['last_name'] =  input('Enter Your Last Name: ').strip().lower()
    contact['phone_number'] =  input('Enter Your phone number: ').strip()
    contact['address'] =  input('Enter Your Last Name: ').strip() 
    return contact

choice = ('a', 'l', 'd', 'e', 'h', 'q')

def you_choiuce():
    return input(F"Make Your choice {choice} => ")

def remove_contact(contact, contacts):
    index = contacts.index(contact)
    confirm = input("Are You sure You want delete this contact? (y/n): ").strip()
    if confirm.lower() in ('yes', 'y'):
        return contacts.pop(index)
    return

def lookup_contact(name, contacts):
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
    old_phone_number = contact['phone_number']
    old_address = contact['address']
    
    first_name = input(f"Enter first name: ({old_first_name}) >>> ").strip().lower() or old_first_name
    last_name = input(f"Enter last name: ({old_last_name}) >>> ").strip().lower() or old_last_name
    phone_number = input(f"Enter phone number: ({old_phone_number}) >>> ").strip() or old_phone_number
    address = input(f"Enter address: ({old_address}) >>> ").strip() or old_address
    
    return {'first_name': first_name.lower(), 'last_name': last_name.lower(), 'phone_number': phone_number, 'address': address}


def save_contact(contacts):
    with open('db.pkl', 'wb') as f:
        pickle.dump(contacts, f)

def load_contact(db_name='db.pkl'):
    unpiclled = []
    # with open('db.pkl', 'rb') as f:
    with open(db_name, 'rb') as f:
        unpiclled = pickle.load(f)
    return unpiclled

def main(db_name):
    # print(f"This is a {__name__} script")
    hello()
    # contacts = load_contact()
    while True:
        match you_choiuce():
            case 'a':
                contacts.append(add_contact())
                save_contact(contacts)
            case 'l':
                contacts = load_contact()
                contacts_list(contacts)
            case 'e':
                contacts = load_contact()
                name = input("Whot are You looking for? ")
                contact = lookup_contact(name, contacts)
                index = contacts.index(contact)
                contact = update_contact(contact)
                contacts[index] = contact
                save_contact(contacts)
            case 'd':
                contacts = load_contact()
                name = input("Whot are You looking for? ")
                contact = lookup_contact(name, contacts)
                # remove_contact(contact)
                contact = remove_contact(contact, contacts)
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
                    
                    
if __name__ == "__main__":
    # print(sys.argv)
    # print(sys.argv[1])
    if (args_cont := len(sys.argv)) > 2:
        print(f"One argument expected, got {args_cont -1}")
        raise SystemExit(1)
    elif args_cont < 2:
        print(f"You must specify the database name")
        raise SystemExit(1)
    db_name = sys.argv[1]
    print(db_name)
    main(db_name)
    