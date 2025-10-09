"""Usage: thingy [OPTIONS]
    -h Display this usage message
    -H hostname Hostname to connect to
    forom math import sqrt
"""

TITLE = "Calculator"

# c = a + b

ok = True
a = input("Enter a = ")
try:
    a = int(a)
except:
    print("It is not a number")
    ok = False
    exit()
    
b = input("Enter b = ")
try:
    b = int(b)
except:
    print("It is not a number")
    ok = False
    exit()
 
if ok != True:
    print("It is number")
    exit()

# o = input("Enter operation = ")
choice = ('+', '-', '*', '/', '//', '%', '**', 'h', 'q')

def you_choiuce():
    return input(F"Make Your choice {choice} => ")

def div():
    """This function div"""
    
    pass

# while True:
    
#     if (o == '+'):
#         c = int(a) + int(b)
#         print("a + b = ", c)
#     elif (o == '-'):
#         c = int(a) - int(b)
#         print("a - b = ", c)
#     elif (o == '*'):
#         c = int(a) * int(b)
#         print("a * b = ", c) 
#     elif (o == '/'):
#         c = int(a) / int(b)
#         print("a / b = ", c)
#     elif (o == '%'):
#         c = int(a) % int(b)
#         print("a % b = ", c)
#     elif (o == '//'):
#         c = int(a) // int(b)
#         print("a // b = ", c)
#     elif (o == '**'):
#         c = int(a) ** int(b)
#         print("a ** b = ", c)
#     elif (o == 'q'):
#         print(f"thenks for using {TITLE}")
#         break
#     else:
#         print("Unkow operation")

# choice = you_choiuce()

def help_me():
    print(
        '''All operation You can do:
            +: a + b
            -:
            *:
            /: a / b
            q: Exot app
        
        '''
    )
    
while True:
    match you_choiuce():
        case '+':
            c = int(a) + int(b)
            print("a + b = ", c)
        case '-':
            pass
        case '*':
            pass
        case '/':
            pass
        case '%':
            pass
        case '//':
            pass
        case '**':
            pass
        case 'q':
            break
        case 'h':
            help_me()
        case _:
            help_me()
        