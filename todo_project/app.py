def my_decor(fn):
    def wrapper():
        func = fn()
        make_upper_case = func.upper()
        return make_upper_case
    return wrapper

def hi():
    return f"hello there"

decorate = my_decor(hi)

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

print(hi_name("Developer"))
        
