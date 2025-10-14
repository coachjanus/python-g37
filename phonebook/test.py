# Dictionary can be created by placing a sequence of elements within curly {} braces, 
# separated by a 'comma'.
d1 = {1: 'Geeks', 2: 'For', 3: 'Geeks'}

capital_city = {"Nepal": "Kathmandu", "Ukraine": "Kyiv", "Italy": "Rome"}
print(capital_city)
numbers = {1: "One", 2: "Two", 3: "Three"}
print(numbers)

# create dictionary using dict() constructor

d2 = dict(a = "Geeks", b = "for", c = "Geeks")

# Access using key

d = { "name": "Prajjwal", 1: "Python", (1, 2): [1,2,4] }


contact = {
    'first_name': 'john',
    'last_name': 'doe',
    'mobile': '1234567'
}

contacts.append(contact)

# for key in contact:
#     print(key)
    
for key in contact:
    print(contact[key])
# print(contacts)
# print(dir(contacts))
# print(contact)
# print(type(contact))
# print(id(contact))
# print(dir(contact))
# print(contacts[0])
# print(contacts[len(contacts) - 1])

​

# Access using key

print(d["name"])

​

# Access using get()

print(d.get("name"))

# Adding a new key-value pair

d["age"] = 22
capital_city["Japan"] = "Tokyo"
 
print("Updated Dictionary: ",capital_city)

​

# Updating an existing value

d[1] = "Python dict"

​
student_id = {111: "Eric", 112: "Kyle", 113: "Butters"}
print("Initial Dictionary: ", student_id)
 
student_id[112] = "Stan"
 
print("Updated Dictionary: ", student_id)

print(d)

# Using del to remove an item

del d["age"]

print(d)

​

# Using pop() to remove an item and return the value

val = d.pop(1)

print(val)

​

# Using popitem to removes and returns

# the last key-value pair.

key, val = d.popitem()

print(f"Key: {key}, Value: {val}")

​

# Clear all items from the dictionary

d.clear()

print(d)

# Iterate over keys

for key in d:

    print(key)

​
# Ітерація по словнику
squares = {1: 1, 3: 9, 5: 25, 7: 49, 9: 81}
for i in squares:
    print(squares[i])
# Iterate over values

for value in d.values():

    print(value)

​

# Iterate over key-value pairs

for key, value in d.items():

    print(f"{key}: {value}")

# Nested Dictionaries


d = {1: 'Geeks', 2: 'For',

        3: {'A': 'Welcome', 'B': 'To', 'C': 'Geeks'}}

​

print(d)

students = {}

​

students['student1'] = {'name': 'Drake', 'age': 20, 'grade': 'A'}

students['student2'] = {'name': 'Travis', 'age': 22, 'grade': 'B'}

students['student3'] = {'name': 'Charlie', 'age': 21, 'grade': 'A+'}

​

print("Student Details:")

print(students)

person = {'employee1': {'name': 'Janice', 'age': 25}}

​

# Adding a new key-value pair to existing inner dictionary

person['employee1']['department'] = 'HR'

​

# Adding a new inner dictionary

person['employee2'] = {'name': 'Jake', 'age': 30, 'department': 'IT'}

​

print("Updated Nested Dictionary:")

print(person)

# Accessing elements

print("Name:", student['student1']['name'])

print("Grade:", student['student1']['grade'])

# Deleting a key from inner dictionary

del employee['emp1']['dept']

​

# Deleting an entire inner dictionary

del employee['emp2']

​

print("Updated Nested Dictionary:")

print(employee)


# Методи для роботи зі словниками в Python
# Функція     Опис
# all()   Повертає True, якщо всі ключі словника дорівнюють True (або якщо словник порожній).
# any()   Повертає True, якщо хоч один із ключів словника дорівнює True. Якщо словник порожній, повертається False.
# len()   Повертає довжину (кількість елементів) словника.
# sorted()    Повертає новий відсортований список ключів у словнику.
# clear()     Видаляє всі елементи зі словника.
# keys()  Повертає новий об’єкт ключів словника.
# values()    Повертає новий об’єкт значень словника.

squares = {1: 1, 3: 9, 5: 25, 7: 49, 9: 81}
 
# Перевірка ключа
print(1 in squares) # виведе True
 
# Перевірка ключа
print(2 not in squares) # виведе True
 
# Перевірка ключа
print(49 in squares) # виведе False, оскільки перевірка проводиться лише для ключів

# 1. Метод clear() словника

# Метод clear() у Python – це вбудований метод, який використовується для видалення всіх елементів (пар ключ-значення) зі словника. Він фактично очищує словник, залишаючи його без пар ключ-значення.
my_dict = {'1': 'Geeks', '2': 'For', '3': 'Geeks'}
my_dict.clear()
print(my_dict)
# 2. Dictionary get() Method

# In Python, the get() method is a pre-built dictionary function that enables you to obtain the value linked to a particular key in a dictionary. It is a secure method to access dictionary values without causing a KeyError if the key isn't present.

d = {'Name': 'Ram', 'Age': '19', 'Country': 'India'}
print(d.get('Name'))
print(d.get('Gender'))

# 3. Dictionary items() Method

# In Python, the items() method is a built-in dictionary function that retrieves a view object containing a list of tuples. Each tuple represents a key-value pair from the dictionary. This method is a convenient way to access both the keys and values of a dictionary simultaneously, and it is highly efficient.

d = {'Name': 'Ram', 'Age': '19', 'Country': 'India'}
print(list(d.items())[1][0])
print(list(d.items())[1][1])

# 4. Dictionary keys() Method

The keys() method in Python returns a view object with dictionary keys, allowing efficient access and iteration.
# 4. Метод keys() словника

d = {'Name': 'Ram', 'Age': '19', 'Country': 'India'}
print(list(d.keys()))

# 5. Dictionary update() Method

# Python's update() method is a built-in dictionary function that updates the key-value pairs of a dictionary using elements from another dictionary or an iterable of key-value pairs. With this method, you can include new data or merge it with existing dictionary entries.
d1 = {'Name': 'Ram', 'Age': '19', 'Country': 'India'}
d2 = {'Name': 'Neha', 'Age': '22'}

d1.update(d2)
print(d1)
# 6. Dictionary values() Method

# The values() method in Python returns a view object containing all dictionary values, which can be accessed and iterated through efficiently.

d = {'Name': 'Ram', 'Age': '19', 'Country': 'India'}

print(list(d.values()))

# 7. Dictionary pop() Method

# In Python, the pop() method is a pre-existing dictionary method that removes and retrieves the value linked with a given key from a dictionary. If the key is not present in the dictionary, you can set an optional default value to be returned.
d = {'Name': 'Ram', 'Age': '19', 'Country': 'India'}

d.pop('Age')

print(d)
# 8. Dictionary popitem() Method

# The popitem() method in Python dictionaries is used to remove and return the last inserted key-value pair as a tuple. If the dictionary is empty then it raises a KeyError.
d = {'Name': 'Ram', 'Age': '19', 'Country': 'India'}

val = d.popitem()

print(val)

​

val = d.popitem()

print(val)

def contact_list():
    if len(contacts) > 0:
        for item in contacts:
            for k,v in item.items():
                print(k, ' => ', v) 
    else:
        print("Your contact list is empty. Go back to menu and add new contact.")

def add_contact():
    contact = {}
    first_name = input("Enter firstr name: ").strip().lower()
    last_name = input("Enter last name: ").strip().lower()
    mobile = input("Enter phoner phone number: ").strip()
    contact['first_name'] = first_name
    contact['last_name'] = last_name
    contact['mobile'] = mobile
    return contact

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

