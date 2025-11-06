# 

# Можна призначити функцію змінній і далі використовувати цю змінну так само, як і саму функцію:
# def func():
#    print("I am function func()!")
# func()
# another_name = func # створює нове посилання на func() під назвою another_name.
# another_name() # можна викликати функцію за назвою, func або another_name

# def foo():
#     print('I am foo function')
    
# foo()

# bar = foo

# bar()

# Цей лямбда-вираз визначає безіменну функцію, яка приймає рядок і повертає реверс рядка

# print(lambda s: s[::-1]) # <function <lambda> at 0x7fef8b452e18>
# У цьому випадку список параметрів складається з одного параметра s.
# s[::-1] - це зріз, що повертає символи з s у зворотному порядку.

# Якщо об’єкт можна викликати за допомогою оператора об'єкт(), цей об’єкт є callable: Об’єкт callable завжди повертає значення. 
# Щоб перевірити, чи можна викликати об’єкт, можна скористатися вбудованою функцією callable(об'єкт). Функція callable повертає True, якщо об’єкт можна викликати, інакше повертає False.
# лямбда-вираз є callable функцією - значення, яке повертає лямбда-вираз, можна викликати.
# Усі вбудовані функції можна викликати. Наприклад, print, len, even callable.

# print(callable(print))
# print(callable(12))
# # Визначені користувачем функції, або лямбда, можна викликати:
def add(a, b):
   return a + b
# print(callable(add)) # Правда
# print(callable(lambda x: x*x)) # Правда
# # Вбудовані методи, такі як a_str.upper, a_list.append, можна викликати. Наприклад:
# str = 'Python Callable'
# print(callable(str.upper)) # Правда

# print(callable(lambda s: s[::-1])) # True

# print(lambda s: s[::-1])

# print(callable(lambda s: s[::-1]))



# Об’єкт, створений лямбда-виразом, є функцією першого порядку, як і будь-який інший об’єкт у Python. Ви можете призначити його змінній, а потім викликати функцію, використовуючи це ім’я:

# reverse = lambda s: s[::-1]

# print(reverse("I am a string")) # 'gnirts a ma I'


# # визначення функції reverse():
# def reverse(s):
#   return s[::-1]

# # Виклики поводяться однаково.
# print(reverse("I am a string")) # 'gnirts a ma I'
# # Лямбда-вираз зазвичай має список параметрів, що не є обов’язково.# лямбда-функція для обчислення середнього трьох чисел.
# print((lambda x1, x2, x3: (x1 + x2 + x3) / 3)(9, 6, 6)) # 7.0

# # Можна визначити лямбда-функцію без параметрів:
# forty_two_producer = lambda: 42
# print(forty_two_producer() / 3) # 14.0
# # Повернене значення лямбда-виразу може бути лише одним виразом.

# # Лямбда-вираз не може містити такі оператори, як assignment або return, а також керуючі структури, такі як for, while, if, else або def.
# # Якщо оператор return містить кілька значень, тоді Python пакує їх і повертає як кортеж:
# def func(x):
#   return x, x ** 2, x ** 3
# print(func(3)) #(3, 9, 27)
# # This implicit tuple packing doesn’t work with an lambda function: (lambda x: x, x ** 2, x ** 3)(3)
# # <stdin>:1: SyntaxWarning: 'tuple' object is not callable; perhaps you missed a comma?
# # Проте можна повернути кортеж з лямбда-функції, явно позначивши кортеж дужками.
print((lambda x: (x, x ** 2, x ** 3))(3)) # (3, 9, 27)
# # також можна повернути список або словник з лямбда-функції:
print((lambda x: [x, x ** 2, x ** 3])(3)) # [3, 9, 27]
print((lambda x: {1: x, 2: x ** 2, 3: x ** 3})(3)) # {1: 3, 2: 9, 3: 27}
# print((lambda x1, x2, x3:(x1 + x2 + x3)) / 3)(8, 7, 6) # 7.0
# def fn(x):
#     return x, x**2, x**3

# print(fn(4))

# print((lambda x: (x, x**2, x**3))(4))

# print((lambda x: [x, x**2, x**3])(4))
# print((lambda x: {1:x, 2:x**2, 3:x**3})(4))

