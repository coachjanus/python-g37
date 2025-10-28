'''

'''
from .db import get_all_contacts, insert_contact, update_contact, delete_contact

TITLE = "phone book"

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
    
def your_choice():
    return input(f"Please make Your choice (l|a|u|d|h|q) >>> ")

def prompt_for_lookup():
    return input("What You looking for? ")

def add_contact(db_name):
    contact = {}
    
    first_name = input("Enter firstr name: ").strip().lower()
    last_name = input("Enter last name: ").strip().lower()
    mobile = input("Enter phoner phone number: ").strip()
    
    contact['first_name'] = first_name
    contact['last_name'] = last_name
    contact['mobile'] = mobile
    
    insert_contact(db_name, contact)

def remove_contact(db_name):
    contacts = get_all_contacts(db_name)
    name = prompt_for_lookup()
    contact = lookup_contact(contacts, name)
    
    confirm = input("Are You sure You want delete this contact? (y/n): ").strip()
    if confirm.lower() in ('yes', 'y'):
        return delete_contact(db_name, contacts, contact)
    return

def lookup_contact(contacts, name):
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
        
def edit_contact(db_name):
    contacts = get_all_contacts(db_name)
    name = prompt_for_lookup()
    contact = lookup_contact(contacts, name)
    
    old_first_name = contact['first_name']
    old_last_name = contact['last_name']
    old_mobile = contact['mobile']
    
    first_name = input(f"Enter first name: ({old_first_name}) >>> ").strip().lower() or old_first_name
    last_name = input(f"Enter last name: ({old_last_name}) >>> ").strip().lower() or old_last_name
    mobile = input(f"Enter phone number: ({old_mobile}) >>> ").strip() or old_mobile
    
    update_contact(db_name, contacts, contact, {'first_name': first_name.lower(), 'last_name': last_name.lower(), 'mobile': mobile})
    
def contact_list(db_name):
    contacts = get_all_contacts(db_name)
    if len(contacts) > 0:
        for item in contacts:
            for k,v in item.items():
                print(k, ' => ', v) 
    else:
        print("Your contact list is empty. Go back to menu and add new contact.")
