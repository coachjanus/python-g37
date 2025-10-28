'''

'''

import pickle

def create_db(db_name):
    try:
        with open(db_name, 'xb') as f:
            pickle.dump([], f)
    except FileExistsError:
        pass

def save_contacts(db_name, contacts):
    with open(db_name, 'wb') as f:
        pickle.dump(contacts, f)

def get_all_contacts(db_name):
    with open(db_name, 'rb') as f:
        return pickle.load(f)
        
def insert_contact(db_name, contact):
    contacts = get_all_contacts(db_name)
    contacts.append(contact)
    save_contacts(db_name, contacts)
    
def update_contact(db_name, contacts, contact, updated):
    contact.update(updated)
    save_contacts(db_name, contacts)
    
def delete_contact(db_name, contacts, contact):
    index = contacts.index(contact)
    result = contacts.pop(index)
    save_contacts(db_name, contacts)
    return result
    