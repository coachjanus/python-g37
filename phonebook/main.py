"""_summary_
"""

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

def contacts_list():
    if len(contacts) > 0:
        for contact in contacts:
            # print(f"{contacts.index(contact)} First Name: {contact['first_name']} Phonew number: {contact['phone_number']} Address: {contact['address']}")    
            print(f"{contacts.index(contact)} Name: {fool_name(contact)} Phonew number: {contact['phone_number']} Address: {contact['address']}")    
    else:
        print("No item in contacts yet")
        
def fool_name(contact):
    return contact['first_name'].title() + " " + contact['last_name'].title()

def add_contact():
    
    contact = {}
    contact['first_name'] =  input('Enter Your First Name: ').strip().lower()
    contact['last_name'] =  input('Enter Your Last Name: ').strip().lower()
    contact['phone_number'] =  input('Enter Your phone number: ').strip()
    contact['address'] =  input('Enter Your Last Name: ').strip() 
    return contact


def lookup_contact():
    pass

def edit_contact():
    pass

choice = ('a', 'l', 'd', 'e', 'h', 'q')

def you_choiuce():
    return input(F"Make Your choice {choice} => ")

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
    old_phone_number = contact['phone_number']
    old_address = contact['address']
    
    first_name = input(f"Enter first name: ({old_first_name}) >>> ").strip().lower() or old_first_name
    last_name = input(f"Enter last name: ({old_last_name}) >>> ").strip().lower() or old_last_name
    phone_number = input(f"Enter phone number: ({old_phone_number}) >>> ").strip() or old_phone_number
    address = input(f"Enter address: ({old_address}) >>> ").strip() or old_address
    
    return {'first_name': first_name.lower(), 'last_name': last_name.lower(), 'phone_number': phone_number, 'address': address}


def main():
    # print(f"This is a {__name__} script")
    hello()
    while True:
        match you_choiuce():
            case 'a':
                contact = add_contact()
                contacts.append(contact)
            case 'l':
                contacts_list()
            case 'e':
                name = input("Whot are You looking for? ")
                contact = lookup_contact(name)
                index = contacts.index(contact)
                contact = update_contact(contact)
                contacts[index] = contact
            case 'd':
                name = input("Whot are You looking for? ")
                contact = lookup_contact(name)
                remove_contact(contact)
            case 'h':
                help_me()
            case 'q':
                bye()
                break
            case _:
                help_me()
                    
                    
if __name__ == "__main__":
    main()