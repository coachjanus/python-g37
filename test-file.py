import os
from pathlib import Path

# Модуль OS використовується для взаємодії з функціями операційної системи, зокрема — для керування файлами та каталогами.

# Щоб створити каталог, передайте шлях до каталогу як параметр функції os.mkdir():

# os.mkdir('my_dir/my_sub_dir')

# Якщо каталог уже існує, os.mkdir() викликає FileExistsError. 

# FileExistsError: [Errno 17] File exists: '.'
# [Errno 17] File exists: '.'
# Щоб уникнути подібних помилок, виловіть помилку, коли вона станеться:

# Крім того, ви можете створити каталог за допомогою pathlib:

p = Path('my_dir/my_sub_dir')
# p.mkdir()

# try:
#     p.mkdir()
# except FileExistsError as e:
#     print(e)

# Крім того, ви можете проігнорувати FileExistsError, передавши аргумент exist_ok=True у .mkdir():
# p.mkdir(exist_ok=True)
# Це не призведе до помилки, якщо каталог уже існує.

# try:
#     Path('example').mkdir()
# except FileExistsError as e:
#     print(e)
    
# p.mkdir(exist_ok=True) 


# Метод os.makedirs() схожий на os.mkdir(). Різниця між ними полягає в тому, що os.makedirs() не тільки може створювати окремі каталоги, але також може використовуватися для створення дерев каталогів. Іншими словами, він може створити будь-які необхідні проміжні папки, щоб забезпечити існування повного шляху.

# Метод os.makedirs() подібний до запуску mkdir -p у Bash. Наприклад, щоб створити групу каталогів, наприклад 2025/10/05, все, що вам потрібно зробити, це:

# os.makedirs('2024/10/25', mode=0o770, exist_ok=True)
# Це створить вкладену структуру каталогів, яка містить папки 2025, 10 і 05:
#  .
#  |
# └── 2025/
# 	└── 10/
#     		└── 05/


# Метод .makedirs() створює каталоги з дозволами за замовчуванням. Якщо вам потрібно створити каталоги з різними дозволами, викличте .makedirs() і перейдіть у режим, у якому ви б хотіли створити каталоги:

# os.makedirs('2025/03/20', mode=0o770, exist_ok=True)

# Це створює структуру каталогу 2025/03/20 і надає власнику та користувачам групи дозволи на читання, запис і виконання. Режим за замовчуванням - 0o777, і біти дозволів файлів існуючих батьківських каталогів не змінюються. 

# Запустіть tree, щоб підтвердити, що застосовано правильні дозволи: $ tree -p -i .
# Передача tree аргументів -p та -i друкує назви каталогів та інформацію про дозволи файлів у вертикальному списку. -p друкує права доступу до файлу, а -i створює вертикальний список дерева без рядків відступу. Як бачите, усі каталоги мають 770 дозволів.

# Альтернативним способом створення каталогів є використання .mkdir() із pathlib.Path:

# p = pathlib.Path('2025/03/20')
# p.mkdir(parents=True, exist_ok=True)

# Передача Parents=True у Path.mkdir() створює каталог 2025 і будь-які батьківські каталоги, необхідні для того, щоб зробити шлях дійсним.

# За замовчуванням os.makedirs() і Path.mkdir() викликають OSError, якщо цільовий каталог уже існує. Цю поведінку можна перевизначити (починаючи з Python 3.2), передавши exist_ok=True як аргумент ключового слова під час виклику кожної функції.



# Термін touch(дотик) означає дію створення порожнього файлу або оновлення позначки часу існуючого файлу. Ця операція знаходить своє значення в багатьох випадках використання, починаючи від завдань системного адміністрування і закінчуючи сценаріями автоматизації.

# У Python модуль pathlib забезпечує зручний та об’єктно-орієнтований підхід до обробки шляхів файлової системи. Клас Path у pathlib представляє шлях до файлової системи та надає різні методи для взаємодії з файлами та каталогами; одним із таких методів є touch().

# Метод touch() використовується для створення порожнього файлу за вказаним шляхом. Якщо файл уже існує, метод оновлює мітки часу доступу та модифікації файлу.

dirnames = ("2025", "2025/10", "2025/10/25")
filenames = ['hello_world.txt', 'random_file.txt', 'lol.txt']

# for dirname in dirnames:
#     for filename in filenames:
#         Path(dirname+"/"+filename).touch()


# Модуль os надає підмодуль під назвою path, який містить кілька методів для виконання операцій із шляхами до файлів. Метод exists() перевіряє існування певного файлу чи каталогу.

# if os.path.exists('/path/to/file'):
#     print('The file exists')
# else:
#     print('The file does not exist')

# Можна безпосередньо перевірити, чи існує шлях до файлу:
# exists = os.path.isfile('/path/to/file')

# if exists:
#     # Store configuration file values
# else:
#     pass
#     # Keep presets

with os.scandir('2025') as hf:
    for h in hf:
        if h.is_file():
            print(h.name)
            
# Ви можете видаляти окремі файли, каталоги та цілі дерева каталогів за допомогою методів, які є в модулях os, shutil і pathlib. Щоб видалити один файл, використовуйте pathlib.Path.unlink(), os.remove(). або os.unlink().  Методи os.remove() і os.unlink() семантично ідентичні. 

# Щоб видалити файл за допомогою os.remove(), виконайте такі дії:

# data_file = 'C:\\Users\\vuyisile\\Desktop\\Test\\data.txt'
# os.remove(data_file)


# Виклик .unlink() або .remove() для файлу видаляє файл із файлової системи. 

# Ці дві функції викличуть OSError, якщо шлях, переданий до них, вказує на каталог замість файлу. Щоб уникнути цього, ви можете або перевірити, чи те, що ви намагаєтесь видалити, насправді є файлом, і видалити його, лише якщо це так, або ви можете використати обробку винятків для обробки OSError:

# data_file = 'home/data.txt'

# # If the file exists, delete it
# if os.path.isfile(data_file):
#    os.remove(data_file)
# else:
#    print(f'Error: {data_file} not a valid filename')

# Щоб видалити файл за допомогою os.unlink(), виконайте такі дії:

# data_file = 'C:\\Users\\vuyisile\\Desktop\\Test\\data.txt'
# os.unlink(data_file)

# Стандартна бібліотека пропонує такі функції для видалення каталогів:
# 	os.rmdir()
# 	pathlib.Path.rmdir()
# 	shutil.rmtree()
# Щоб видалити один каталог або папку, скористайтеся os.rmdir() або pathlib.rmdir(). Ці дві функції працюють, лише якщо каталог, який ви намагаєтеся видалити, порожній. Якщо каталог не порожній, виникає повідомлення OSError:
import shutil

trash_dir = '2024'
# try:
#    os.rmdir(trash_dir)
# except OSError as e:
#    print(f'Error: {trash_dir} : {e.strerror}')

# Якщо каталог не порожній, на екран виводиться повідомлення про помилку:

# Traceback (most recent call last):
#   File '<stdin>', line 1, in <module>
# OSError: [Errno 39] Directory not empty: 'my_documents/bad_dir'


# trash_dir = Path('my_documents/bad_dir')

# try:
#    trash_dir.rmdir()
# except OSError as e:
#    print(f'Error: {trash_dir} : {e.strerror}')

# Щоб видалити непорожні каталоги та цілі дерева каталогів, Python пропонує shutil.rmtree():

# import shutil

# trash_dir = 'my_documents/bad_dir'

# try:
#    shutil.rmtree(trash_dir)
# except OSError as e:
#    print(f'Error: {trash_dir} : {e.strerror}')

# Усе в trash_dir видаляється, коли для нього викликається shutil.rmtree(). 



# Об’єкт Python вважається ітератором, якщо він реалізує два спеціальні методи, відомі як протокол ітератора. Ці два методи забезпечують роботу ітераторів Python. 
# Метод .__iter__() викликається для ініціалізації ітератора та повертає об’єкт-ітератор.
# Метод  .__next__() викликається для повторення ітератора і повертає наступне значення в потоці даних.
# Метод .__iter__() ітератора повертає посилання на поточний об’єкт: об’єкт ітератора - поточний екземпляр. 
# Метод .__next__() повертає наступний елемент із потоку даних. Він також має викликати виняток StopIteration, коли в потоці даних більше немає доступних елементів. Цей виняток завершує ітерацію. Ітератори використовують винятки для керування потоком.

# Iterable - це об’єкт, який можна передати у вбудовану функцію iter(), щоб отримати з нього ітератор. Внутрішньо iter() звертається до виклику .__iter__() для цільових об’єктів. Якщо вам потрібен швидкий спосіб визначити, чи є об’єкт ітерованим, використовуйте його як аргумент iter(). Якщо ви отримуєте ітератор, то ваш об’єкт можна ітерувати. Якщо ви отримуєте помилку, це означає, що об’єкт не можна ітерувати:
# numbers = [1, 2, 3, 4, 5]
# iter_numbers = iter(numbers)
# print(iter_numbers) # <list_iterator object at 0x105858760>
# iter(42)
# Traceback (most recent call last):
# TypeError: 'int' object is not iterable
# Коли ви передаєте ітерований об’єкт як аргумент вбудованої функції iter(), ви отримуєте ітератор для об’єкта. Навпаки, якщо ви викликаєте iter() з об’єктом, який не можна ітерувати, як-от ціле число, ви отримуєте виняток TypeError.

# Вбудований модуль OS має низку функцій, які можна використовувати для переліку вмісту каталогу та фільтрації результатів. Щоб отримати список всіх файлів і папок у певному каталозі файлової системи, використовуйте os.listdir() або os.scandir() у Python 3.x. 

# Перелік файлів в поточному каталозі за допомогою listdir: print(os.listdir())
# os.scandir() є кращим методом для використання, якщо ви також хочете отримати властивості файлу та каталогу, такі як розмір файлу та дата зміни.

# Перелік файлів в поточному каталозі за допомогою os.scandir():
# entries = os.scandir('my_directory/') # <posix.ScandirIterator object at 0x7f5b047f3690>
# Використання os.scandir() з оператором with, автоматично звільняє отримані ресурси після того, як ітератор вичерпано:
# with os.scandir('my_directory/') as entries:
#     for entry in entries:
#         print(entry.name)

# Об’єкти pathlib.Path() мають метод .iterdir() для створення ітератора всіх файлів і папок у каталозі. 
# Метод Path().iterdir() дозволяє переглядати всі файли та підкаталоги в папці і повертає вміст каталогу:
# for entry in Path('.').iterdir():
#     print(entry.name)
# Це особливо корисно для обробки всіх файлів у каталозі або виконання операцій над кожним записом.

# Метод .iterdir() створює ітератор, який перераховує файли випадковим чином.
# Оскільки iterdir() повертає ітератор, записи витягуються на вимогу, коли ви проходите через цикл. Метод is_dir() повертає True, якщо шлях вказує на каталог, і False в іншому випадку.
# for entry in cwd.iterdir():
#    if entry.is_dir():
#        print(entry.name)

# Абстракція списків або спискове включення (List Comprehension) - це спосіб компактного опису операцій обробки списків. Comprehension походить від латинського слова prehendō (схопити - схопити, схопити - обхопити, затримати - перехватити, захопити зненацька, взяти корінь - захопити).
# List Comprehensions розглядається як частина функціонального програмування в Python, дозволяє створювати списки з меншою кількістю кода. 
# list comprehension [expression for member in iterable] включає три елементи:
# expression - математична операція, результат якої буде збережено в новому списку. 
# member - об’єкт або значення в списку чи ітерації. 
# iterable - список, набір, послідовність, генератор або об’єкт, що повертає елементи по одному. 
# Comprehension використовується для створення нових списків, словників і наборів із існуючих ітерованих даних. Comprehension перебирає вхідний контейнер даних і генерує новий контейнер.

# numbers = [1, 2, 3, 4]
# [number**3 for number in numbers]
# [1, 8, 27, 64]

numbers = [1,2,3,4,5,6,7,8,9]
# print([n**3 for n in numbers])

# Умовний оператор може перевірити будь-який дійсний вираз. 
# <value-if-condition-is-true> if <condition> else <value-if-condition-is-false>
# Найпоширенішим способом додати умовну логіку до list comprehension є умова в кінці виразу:
print([x for x in range(100) if x % 2 == 0])

# Умовні оператори дозволяють відфільтрувати непотрібні значення 
# my_list = [2, 5, -4, 6]
# output = [item for item in my_list if item < 0]  # [-4]
# print(output)
# # еквівалент циклу може виглядати так:
# output = []
# for item in my_list:
#    if item < 0:
#        output.append(item)
# print(output)

# print([n for n in numbers if n%2 == 0])

# for file in [i for i in os.scandir('2025') if os.path.isfile(i)]:print(file.name)

# dirname = '2025'

# for root, dirs, files in os.walk(dirname):
#     for dir_name in dirs:
#         print(os.path.join(root, dir_name))
#     for file_name in files:
#         print(os.path.join(root, file_name))


# Щоб створити лише список файлів зі списку каталогів, використовуйте is_file:

# List all files in a directory using scandir()
# with os.scandir('.') as entries:
#     for entry in entries:
#         if entry.is_file():
#             print(entry.name)
# Виклик entry.is_file() для кожного елемента повертає True, якщо об’єкт є файлом. 

# Код можна зробити більш лаконічним, якщо об’єднати цикл for і оператор if в list comprehension:
# for file in [item for item in os.listdir('.') if os.path.isfile(item)]:
#      print(file) # step 1
# # Використання os.scandir(): 
# for file in [item for item in os.scandir('.') if os.path.isfile(item)]:
#      print(file.name)


# Щоб виконати навігацію по файловій системі, потрібно застосувати функцію os.walk().
# Функція os.walk() проходить по всіх файлах та папках у зазначеній директорії та надає три значення: (1) поточна папка, (2) список підпапок та (3) список файлів ;

# def main():
#    directory = "today_directory"
#    for root, dirs, files in os.walk(directory):
#        print("Start dir:", root)
#        print("Nested dirs:")
      
#        for dir_name in dirs:
#            print(os.path.join(root, dir_name))
          
#        print("Files:")
#        for file_name in files:
#            # використовується os.path.join() для отримання повного шляху до файлу або папки.
#            print(os.path.join(root, file_name))


# def getFiles(monitor):
#    filesList=[]

#    for x in monitor:
#        if os.path.isdir(x['path']):
#            if x['recursive']:
#                filesList.extend([os.path.join(root, f) for (root, dirs, files) in os.walk(x['path']) for f in files])
#            else:
#                filesList.extend([item for item in os.listdir(x['path']) if os.path.isfile(item)])
#        elif os.path.isfile(x['path']):
#            filesList.append(x['path'])
#    return filesList

# функція os.walk() може заощадити вам ресурси. У процесі звернення до os.walk(), виконується обхід файлової системи із зазначеного стартового шляху. Під час обходу, os.walk() генерує кортежі з інформацією про поточний каталог, вкладені каталоги та файли. При цьому функція os.walk() не повертає всі значення відразу, натомість повертає об’єкт-генератор. Він генерує значення при необхідності, запам’ятовуючи поточний стан. Тобто, якщо у вас є цикл for, ви можете зупинити обхід директорій, якщо в цьому є необхідність, а потім продовжити з цього моменту.
# start_path = '/якийсь/довгий/шлях/до/директорії'
# generator = os.walk(start_path)

# # Перебираємо перші 206 файлів
# for root, dirs, files in generator:
#    for file in files:
#        # Обробка файла
#        print(os.path.join(root, file))
#        # Вимикаємо обхід після 206 файлів
#        if len(files) > 206:
#            break
#    else:
#        continue
#    break

# Запускаємо обхід з того етапу, на якому зупинились

# for root, dirs, files in generator:
#    for file in files:
#        # Обробка файла
#        print(os.path.join(root, file))

# Коли ми використовуємо об’єкт-генератор у циклі for, він автоматично отримує нові значення з os.walk() кожної ітерації. Це означає, що інформація про директорії та файли генерується в міру обходу файлової системи, а не завантажується одразу. 
# 
# У випадках, коли йде обробка великого масиву даних, скажімо, мільйона файлів, такий підхід заощаджує пристойний обсяг пам’яті, необхідний зберігання цих значень.

# Конструктор sha256() використовується для створення хешу SHA256. Конструктор sha256 приймає байтоподібний вхід, повертаючи хешоване значення. 

# Функція encode використовується для перетворення рядка в байти, що можна передати у функцію sha256
# Функція hexdigest використовується для перетворення даних у шістнадцятковий формат SHA256 для рядка

# Хешувати один рядок за допомогою hashlib.sha256

# import hashlib

# a_string = 'this string holds important and private information'

# hashed_string = hashlib.sha256(a_string.encode('utf-8')).hexdigest()
# print(hashed_string)

# Модуль hashlib можна задіяти в парі з функцією os.walk() для пошуку в директоріях файлів-дублікатів. У цьому випадку програма порівнює їх хеш-суми та робить висновок про ідентичність даних:


# def get_file_hash(file_path):
#    """Визначає хеш файла"""
#    with open(file_path, 'rb') as f:
#        data = f.read()
#        file_hash = hashlib.sha256(data).hexdigest()
#    return file_hash
# Функція  get_file_hash() обчислює хеш кожного файлу за алгоритмом SHA-256. Після цього хеш та шлях до файлу зберігаються у словнику file_hashes. Якщо буде знайдено файл з аналогічним хешем, він додасться до списку duplicate_files.


# def find_duplicate_files(start_path):
#    """Виявляє ідентичні файли у вказанному каталозі, а також у всіх вкладених каталогах"""
#    file_hashes = {}  # Словник для хешей файлів
#    duplicate_files = []  # Список для збереження дубликатів файлов
#    for root, dirs, files in os.walk(start_path):
#        for file_name in files:
#            file_path = os.path.join(root, file_name)
#            file_hash = get_file_hash(file_path)
#            if file_hash in file_hashes:
#                duplicate_files.append((file_path, file_hashes[file_hash]))
#            else:
#                file_hashes[file_hash] = file_path
#    return duplicate_files

# start_path = '/path/to/directory'
# duplicates = find_duplicate_files(start_path)
# if duplicates:
#    print("Знайдені дубликати:")
#    for file1, file2 in duplicates:
#        print(file1, "та", file2)
# else:
#    print("Файлів з ідентичним змістом не знайдено")

# Потрібно перейменувати групу файлів у директорії example, додавши до кожного префікс today_:

# start_dir = start_path = 'example'
# add_prefix = 'today_'

# for root, dirs, files in os.walk(start_dir):
#    for file in files:
#        file_path = os.path.join(root, file)
#        edit_file_name = add_prefix + file
#        edit_file_path = os.path.join(root, edit_file_name)
#        os.rename(file_path, edit_file_path)
#        print(file_path, edit_file_name)


# Змінна edit_file_name в коді лишається сталою протягом виконання скрипту. Навіть якщо у файловому менеджері вручну повернути ім’я файлу до початкового стану, змінна edit_file_name залишається з префіксом today_.

# функція os.path.basename() дозволяє зчитати им’я файла без посилання і добавляє префікс коректно:

# for root, dirs, files in os.walk(start_dir):
#    for file in files:
#        if not file.startswith(add_prefix):
#            file_path = os.path.join(root, file)
#            file_name = os.path.basename(file_path)  # отримаємо ім'я файла без його адреси
#            edit_file_name = add_prefix + file_name  # Додаємо префикс до імені файла
#            edit_file_path = os.path.join(root, edit_file_name)
#            os.rename(file_path, edit_file_path)
#            print(file_path, edit_file_name)

# Модуль time входить до стандартної бібліотеки Python.
# визначення поточного часу:
# import time

# time_now = time.time()
# print(time_now)

# Функція time.time повертає число - час (у секундах), який минув з еталонного часу, або епохи. Для більшості систем епохою є четвер, 1 січня 1970 року о 00:00:00 UTC. Дати й час перед цією епохою задаються від’ємним числом. 
# Відображення часу в секундах з 1970 року не є особливо корисним, тому його можна відобразити як попередньо відформатований рядок:

# print(time.ctime(time_now))

# Функцію time() можна використовувати для перевірки часу виконання блоку коду, що може бути дуже цінною інформацією під час написання складних програм. 

# t1 = time.time()
# for i in range(4):
#    print(i)
#    # Функція  sleep() може призупинити виконання програми на певну кількість секунд:
#    time.sleep(1)

# t2 = time.time()
# print('Runtime: %s seconds'%(t2 - t1))

# Тут ми хронометруємо цикл for. 
# У циклі ми просто друкуємо індекс, а потім зупиняємо цикл на 1 секунду. 

# Розуміння словника (Dictionary comprexdigest()
# if file in files and sha256 != files[file]:
#     print(f'{file} has been changed! {time.strftime("%Y-%m-%d %H:%M:%S")}hension) - це метод перетворення одного словника в інший. Під час цього перетворення елементи вихідного словника можна умовно включити до нового словника, і кожен елемент можна трансформувати за потреби.
# Dictionary comprehension надає доступ до ключів та значень словника.
# dict_variable = {key:value for (key,value) in dictionary.items()}
# dict1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
# Метод keys() повертає усі ключі у словнику.
# dict1.keys()# ['c', 'd', 'a', 'b']
# Метод values() повертає усі значення у словнику.
# dict1.values() # [3, 4, 1, 2]
# Метод items() повертає усі пари ключ-значення в словнику
# dict1.items() # [('c', 3), ('d', 4), ('a', 1), ('b', 2)]
# # Double each value in the dictionary
# double_dict1 = {k:v*2 for (k,v) in dict1.items()}
# print(double_dict1)


