"""Usage: thingy [OPTIONS]
    -h Display this usage message
    -H hostname Hostname to connect to
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

o = input("Enter operation = ")

if (o == '+'):
    c = int(a) + int(b)
    print("a + b = ", c)
elif (o == '-'):
    c = int(a) - int(b)
    print("a - b = ", c)
elif (o == '*'):
    c = int(a) * int(b)
    print("a * b = ", c) 
elif (o == '/'):
    c = int(a) / int(b)
    print("a / b = ", c)
elif (o == '%'):
    c = int(a) % int(b)
    print("a % b = ", c)
elif (o == '//'):
    c = int(a) // int(b)
    print("a // b = ", c)
elif (o == '**'):
    c = int(a) ** int(b)
    print("a ** b = ", c)
else:
    print("Unkow operation")
