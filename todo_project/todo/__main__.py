'''
Модуль __main__.py Provides an entry-point script to run the app from the package using the python -m
rptodo command
скрипт точки входу для запуску програми з пакета за допомогою команди python -m rptodo
'''

from todo import cli

def main():
    cli.app()

if __name__ == "__main__":
    main()