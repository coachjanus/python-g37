import os, time

from pathlib import Path

import hashlib

import shelve

# Вбудований модуль shelve

# У Python існує концепція shelf - постійного місця для зберігання об’єкта, який нам може знадобитися прочитати пізніше. Таким чином, модуль shelf схожий на базу даних.
# shelf - це постійний об’єкт, схожий на словник. Різниця з базами даних полягає в тому, що значення на полиці можуть бути  довільними об’єктами Python - будь-чим, що може обробити модуль pickle. Це включає більшість екземплярів класів, рекурсивних типів даних та об’єктів, що містять багато спільних підоб’єктів. Ключі shelf - звичайні рядки.
# За допомогою shelve можна використовувати словник як постійне сховище даних.
# Для використання модуля shelve зазвичай найкраще використовувати оператор with, щоб ми могли уникнути написання виклику close(). Можна зберігати будь-який тип даних, який підтримує pickle, як значення в словнику shelve.
monitor = [
    {
        'path': '2025',
    },
    {
        'path': 'examole'
    }
]

# Щоб прочитати дані з файлу shelve, можна відкрити його в операторі with (менеджер контексту).
# Отримати доступ до значень зі словника shelve можна за допомогою методу get(), який дозволяє вказати значення за замовчуванням.
# Отримання значень з shelve

def getFiles(monitor):
    filesList = []
    
    for x in monitor:
        if os.path.isdir(x['path']):
            filesList.extend([os.path.join(root, f) for (root, dirs, files) in os.walk(x['path']) for f in files])
        elif os.path.isfile(x['path']):
            filesList.append(x['path'])
    return filesList

# Моніторинг каталогів
def main():
    files = {}
    
    while True:
        for file in getFiles(monitor):
            # print(file)
            hash = hashlib.sha256()
            
            with open(file) as f:
                for chunck in iter(lambda: f.read(2048), ''):
                    hash.update(chunck.encode('utf-8'))
                    sha256 = hash.hexdigest()
                    # print(sha256)
                    
                    if file in files and sha256 != files[file]:
                        print(f"{file} has been changed! {time.strftime('%Y-%m-%d %H:%M:%S')}")
                        
                    files[file] = sha256
                    # print(files)
                    
                    with shelve.open('monit.db') as s:
                        s[file] = files[file]
                        
                time.sleep(1)
                
                    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass