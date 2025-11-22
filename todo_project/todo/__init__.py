"""
todo/__init__.py
Top level module for todo application
Програма To Do для складання списків справ,
яка допоможе оптимізувати список справ на день.
"""

__app_name__ = "Todo list"
__version__ = "0.1.0"

# коди повернення за допомогою range() призначаємо їм цілі числа.
(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    JSON_ERROR,
    ID_ERROR,
) = range(7)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    DB_READ_ERROR: "database read error",
    DB_WRITE_ERROR: "database write error",
    ID_ERROR: "to-do id error",
}

MESSAGES = {
    SUCCESS: "operation successful",
    ERRORS[DIR_ERROR]: "config directory error",
    ERRORS[FILE_ERROR]: "config file error",
    ERRORS[DB_READ_ERROR]: "database read error",
    ERRORS[DB_WRITE_ERROR]: "database write error",
    ERRORS[ID_ERROR]: "to-do id error",
}
