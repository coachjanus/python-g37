def make_title(fn):
    def wrapper():
        func = fn()
        output = func.title()
        return output
    return wrapper

@make_title
def to_upper():
    return f"Coose sone category"

def my_decor(fn):
    def wrapper():
        func = fn()
        make_upper_case = func.upper()
        return make_upper_case
    return wrapper

def hi():
    return f"hello there"

# decorate = my_decor(hi)

# print(decorate())

import sys

def command_decor(fn):
    def wrapper(arg=None):
        if arg == None:
            print(f"""You get an error, You are missing Name.
                  Usage: app.py [OPTIONS] NAME""")
            raise sys.exit("Missing argument Name")
        func = fn(arg)
        make_upper_case = func.upper()
        return make_upper_case
    return wrapper

@command_decor
def hi_name(name):
    return f"hello there {name}"

# print(hi_name())

# print(hi_name("Developer"))

def decor(fn):
    def wrapper(arg):
        func = fn(arg)
        output = func.title()
        return output
    return wrapper

@decor
def make_title(name):
    return name


def decor_input(fn):
    def wrapper(arg):
        func = fn(arg)
        output = func.strip().upper()
        return output
    return wrapper

@decor_input
def make_upper(string):
    return string
        
# print(make_upper("   hello there world   "))

