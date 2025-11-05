# Прочитати файл data.csv:

import csv

with open('data.csv', newline='') as myFile:
   reader = csv.reader(myFile)
   for row in reader:
       print(row)

# $ python reader.py

# Модуль csv дозволяє створити діалект із специфічними характеристиками файлу CSV:

# Наприклад, ми можемо прочитати файл з іншим роздільником, таким як табуляція, крапка чи навіть пробіли (справді будь-який символ).

csv.register_dialect('myDialect', delimiter='/', quoting=csv.QUOTE_NONE)
with open('csvexample2.csv', newline='') as myFile:
  reader = csv.reader(myFile, dialect='myDialect')
  for row in reader:
      print(row)


# Приклад створює список даних, причому кожен елемент у зовнішньому списку представляє рядок у файлі CSV. 


myData = [[1, 2, 3], ['Good Morning', 'Good Evening', 'Good Afternoon']]
myFile = open('csvexample3.csv', 'w')
with myFile:
  writer = csv.writer(myFile)
  writer.writerows(myData)

# Об’єкт запису також підтримує інші формати CSV:

csv.register_dialect('myDialect', delimiter='/', quoting=csv.QUOTE_NONE)
myFile = open('csvexample4.csv', 'w')
with myFile:
  writer = csv.writer(myFile, dialect='myDialect')
  writer.writerows(myData)

# Ми також можемо створити файл CSV за допомогою словників. 

# Після цього ми спочатку записуємо рядок заголовка за допомогою методу writeheader(), а потім пари значень за допомогою методу writerow(). Позиція кожного значення в рядку вказується за допомогою мітки стовпця. 

myFile = open('countries.csv', 'w')
with myFile:   
   myFields = ['country', 'capital']
   writer = csv.DictWriter(myFile, fieldnames=myFields)   
   writer.writeheader()
   writer.writerow({'country' : 'France', 'capital': 'Paris'})
   writer.writerow({'country' : 'Italy', 'capital': 'Rome'})
   writer.writerow({'country' : 'Spain', 'capital': 'Madrid'})

# Модуль csv надає допоміжні класи, які дозволяють читати/записувати CSV-дані в/з об’єктів словника.
# файл countries.csv з таким вмістом:

# Перший рядок цього файлу містить назви стовпців, які містять мітку для кожного стовпця даних. Рядки в цьому файлі містять пари значень (країна, столиця), розділених комою. Ці мітки необов’язкові, але, як правило, дуже корисні, особливо коли вам потрібно переглядати ці дані.
# Щоб прочитати цей файл, ми створюємо такий код:

with open('countries.csv') as myFile: 
   reader = csv.DictReader(myFile)
   for row in reader:
       print(row['country'])

# тепер ми можемо отримати доступ до стовпців кожного рядка за їхньою міткою - country. Якби ми хотіли, ми також могли б отримати доступ до капіталу за допомогою row['capital'].


# Що робити, якщо розмір файлу перевищує доступну пам’ять? Функція csv_reader() відкриває файл і використовує file.read() разом із .split(), щоб додати кожен рядок як окремий елемент до списку: 

def csv_reader(file_name):
    file = open(file_name)
    result = file.read().split("\n")
    return result

csv_gen = csv_reader("some_csv.txt")
row_count = 0

for row in csv_gen:
    row_count += 1
    print(f"Row count is {row_count}")

# Якщо розмір файлу перевищує доступну пам’ять, буде згенеровано виключення MemoryError, бо  file.read().split() завантажує все в пам’ять одночасно, викликаючи помилку MemoryError.

# Нове визначення csv_reader():

def csv_reader(file_name):
    for row in open(file_name, "r"):
        yield row


# Можна визначити генераторний вираз та використовувати генератор без виклику функції:

csv_gen = (row for row in open('file_name'))
# Це більш стислий спосіб створення списку csv_gen. 

# Функція zip(a, b) створює об'єкт-ітератор, з якого на кожному етапі циклу витягується кортеж, що складається з двох елементів. Перший береться із списку a, другий - із b.
# Функція zip дозволяє пройти одночасно по кількох ітерованим об'єктам:

a = [10, 20, 30, 40]
b = ['a', 'b', 'c', 'd', 'e']
for i in zip(a, b):
    print(i, type(i))

# Якщо два списки мають різну довжину, то довгий будет обрізаний до довжини короткого.
first_names = ['John', 'Jeff', 'Chris']
last_names = ['Wick', 'Chen', 'Test', 'Truncated']

names = zip(first_names, last_names)
for name in names:
    print(name)

# Функція zip повертає ітератор, який зупиняється, коли вичерпується найкоротша послідовність. Якщо потрібно обробляти всі значення, слід використовувати функцію zip_longest  з модуля itertools:

import itertools

a = [10, 20, 30, 40]
b = ['a', 'b', 'c', 'd', 'e']
c = [1.1, 1.2]

for i in itertools.zip_longest(a,b,c):
    print(i)

# Конвертування 2-х списків у словник
column_names = ['id', 'color', 'style']
column_values = [1, 'red', 'bold']
# за допомогою циклу
name_value_tuples = zip(column_names, column_values)
name_to_value_dict = {}

for key, value in name_value_tuples:
    if key in name_to_value_dict:
        pass # Insert logic for handling duplicate keys
    else:
        name_to_value_dict[key] = value
    print(name_to_value_dict)

# інвертувати словник
# Перемикання ключа і значення словника (інвертувати словник)
my_dict = {1: 'a', 2: 'b', 3: 'c'}

swapped = {v: k for k, v in my_dict.items()}
swapped = dict((v, k) for k, v in my_dict.items())
swapped = dict(zip(my_dict.values(), my_dict))
swapped = dict(zip(my_dict.values(), my_dict.keys()))

print(swapped) # Out: {a: 1, b: 2, c: 3}




def reader(file):
    f = open(file)
    result = f.read().split("\n")
    return result

# gen1 = reader('some')
# count = 0
# for row in gen1:
#     count += 1
# print(count)

csv_gen = (row for row in open('some'))

def csv_reader():
    for row in open('some'):
        yield
        
import csv

data = [
    [1,2,3],
    ['foo', 'bar', 'baz']
]

# with open('data1.csv', 'w') as f:
#     writer1 = csv.writer(f)
#     writer1.writerows(data)


# with open('data1.csv', newline='\n') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         print(row)


file_name = 'data.csv'
lines = (line for line in open(file_name))

list_line = (s.rstrip().split(',') for s in lines)

cols = next(list_line)

company_dicts = (dict(zip(cols, data)) for data in list_line)

founding = (
    int(company_dict['raisedAmt'])
    for company_dict in company_dicts 
    if company_dict['round'] == 'a'
)

total_series_a = sum(founding)

print(f"Total series A: ${total_series_a}")

def fac(x):
    a = 1
    for i in range(1, x + 1):
        a *= i
        yield a

for x in fac(100):
    print(x, end=" ")
    
def fibo(n):
    if n in (0,1):
        return n
    return fibo(n-1) + fibo(n-2)

print([fibo(n) for n in range(10)])