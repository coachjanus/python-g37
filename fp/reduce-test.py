# Функція reduce(function, iterable, initial)
# Аргументи: 
# function повинна приймати два аргументи. 
# iterable - ітерація.
# initial(необов’язковий аргумент) містить початкове значення. 
# Виклик reduce() починається із застосування function до перших двох елементів з iterable. 
# reduce обчислює перший кумулятивний результат (акумулятор) Потім reduce() використовує накопичувач і третій елемент в iterable  для обчислення наступного кумулятивного результату. Процес триває, доки функція не поверне єдине значення. Функція буде викликана n-1 раз, якщо список містить n елементів. 
# Щоб використовувати reduce(), вам потрібно імпортувати його з модуля functools.
from functools import reduce
# reduce() застосовує функцію до елементів ітерації по два одночасно,
print(reduce(lambda x, y: x + y, [2, 18, 9, 22, 17, 24, 8, 12, 27])) # 139
print(reduce(lambda acc, x: f'{acc} | {x}', ['cat', 'dog', 'cow'])) #'cat | dog | cow'
reduce(lambda acc, pair: acc + pair[0], [(1, 'a'), (2, 'b'), (3, 'c')], 0) # 6
# Найпростіший виклик reduce() приймає одну функцію та одну ітерацію:

def f(x, y):
  return x + y
# reduce() повертає результат 15 зі списку [1, 2, 3, 4, 5]:
reduce(f, [1, 2, 3, 4, 5]) # 15

# sum() повертає суму числових значень у ітерації:
sum([1, 2, 3, 4, 5]) # 15
# Об’єднує рядки зі списку:
reduce(f, ["cat", "dog", "hedgehog", "gecko"]) # 'catdoghedgehoggecko'
# Це саме те, що робить str.join():
"".join(["cat", "dog", "hedgehog", "gecko"]) # 'catdoghedgehoggecko'

from functools import reduce

print(reduce(lambda x, y: x + y, data))
# Факториал натурального числа n можна реалізувати за допомогою reduce() і range():
def multiply(x, y):
  return x * y

def factorial(n):
  from functools import reduce
  return reduce(multiply, range(1, n + 1))

def factorial(n):
  from functools import reduce
  return reduce(lambda x, y: x * y, range(1, n + 1))
factorial(4) # 24
factorial(6) # 720

def factorial(n):
    return reduce(lambda x, y: x * y, range(1, n +1))

print(factorial(4))

print(factorial(6))

# максимальне значення в списку.
# Для цього в Python передбачено вбудовану функцію max(),
max([23, 49, 6, 32]) # 49

# також можете використовувати reduce():
def greater(x, y):
  return x if x > y else y

reduce(greater, [23, 49, 6, 32]) # 49


# Якщо ви вказуєте початкове значення, тоді reduce() запускає перше часткове обчислення,
# використовуючи початковий і перший елемент iterable.
def f(x, y):
  return x + y

# Reduce function with <init> argument
reduce(f, [1, 2, 3, 4, 5], 100)  # (100 + 1 + 2 + 3 + 4 + 5) # 115

# Using lambda:
reduce(lambda x, y: x + y, [1, 2, 3, 4, 5], 100) # 115

# You could readily achieve the same result without reduce():
100 + sum([1, 2, 3, 4, 5]) # 115

# reduce() об’єднує елементи для створення єдиного результату. цей результат може бути складеним об’єктом, таким як список або кортеж. ви можете реалізувати map() у термінах reduce():
numbers = [1, 2, 3, 4, 5]
list(map(str, numbers)) # ['1', '2', '3', '4', '5']

def custom_map(function, iterable):
  from functools import reduce
  return reduce(
      lambda items, value: items + [function(value)],
      iterable,
      [],
  )
list(custom_map(str, numbers)) # ['1', '2', '3', '4', '5']
# You can implement filter() using reduce() as well:
numbers = list(range(10))
def is_even(x):
  return x % 2 == 0
list(filter(is_even, numbers)) # [0, 2, 4, 6, 8]
def custom_filter(function, iterable):
  from functools import reduce
  return reduce(
      lambda items, value: items + [value] if function(value) else items,
      iterable,
      []
  )
list(custom_filter(is_even, numbers)) # [0, 2, 4, 6, 8]

# Сума парних чисел: filter() і reduce()
numbers = [1, 3, 10, 45, 6, 50]
def is_even(number):
  return number % 2 == 0

# reduce() обчислює суму всіх парних чисел, які надає filter().
even_numbers = list(filter(is_even, numbers))

# reduce() використовує лямбда-функцію
reduce(lambda a, b: a + b, even_numbers) # 66

# як з’єднати filter() і reduce(), щоб отримати той самий результат
reduce(lambda a, b: a + b, filter(is_even, numbers)) # 66
