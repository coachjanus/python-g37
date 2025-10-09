"""_summary_
"""

TITLE = "Phone book"

contacts = []

def help_me():
    pass

def bye():
    print (f"Thanks for using {TITLE}")
    

def hello():
    print (f"Hi! This is {TITLE}")

def contacts_list():
    if len(contacts) > 0:
        for item in contacts:
            # print(f"#{contacts.index(item)} {item.name} {item.phone_number} {item.address}")
            
            name, phone_number, address = item
            print(f"#{contacts.index(item)} Name: {name} Phonew number: {phone_number} Address: {address}")
            # print(f"#{contacts.index(item)} {item}")
    else:
        print("No item in contacts yet")

def add_contact():
    
    name = input("Enter name = ")
    phone_number = input("Enter phone number")
    address = input("Enter address")
    contact = (name, phone_number, address)
    return contact

def remove_contact():
    pass

def lookup_contact():
    pass

def edit_contact():
    pass

choice = ('a', 'l', 'd', 'e', 'h', 'q')

def you_choiuce():
    return input(F"Make Your choice {choice} => ")

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
                pass
            case 'd':
                pass
            case 'h':
                help_me()
            case 'q':
                bye()
                break
            case _:
                help_me()
                    
                    
if __name__ == "__main__":
    main()