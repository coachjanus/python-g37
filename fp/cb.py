
# Можна передати функцію іншій функції як аргумент:

def inner():
  print("I am function inner()!")

def outer(function):
  function()

outer(inner) # inner() як аргумент(параметр) функції outer()
# Це відомо як композиція функції. Коли функція передається іншій функції, функцію-аргумент іноді називають зворотним викликом, оскільки зворотний виклик внутрішньої функції може змінити поведінку зовнішньої функції.

def inner():
    print("I'm inner function")
    
def outer(fn):
    print("I'm oter function")
    fn()

outer(inner)

# Прикладом функції зворотного виклику є функція sorted(), що сортує список у лексичному порядку:
animals = ["ferret", "vole", "dog", "gecko"]
# sorted(animals) #['dog', 'ferret', 'gecko', 'vole']
# # Функція sorted() приймає додатковий ключовий аргумент, який визначає функцію зворотного виклику, що може служити ключем сортування, наприклад, можна сортувати за довжиною рядка:
# sorted(animals, key=len) # ['dog', 'vole', 'gecko', 'ferret']
# # Необов’язковий аргумент reverse визначає сортування у зворотному порядку.
# sorted(animals, key=len, reverse=True) # ['ferret', 'gecko', 'vole', 'dog']
# Можна визначити власну функцію зворотного виклику, яка змінює значення len():
# def reverse_len(s):
#   return -len(s)
# sorted(animals, key=reverse_len) # ['ferret', 'gecko', 'vole', 'dog']
# # Функція sorted() не змінює послідовність, а повертає нову відсортовану.
# print("повертає нову відсортовану послідовність: ", sorted(animals, reverse=True))
# print("повертає новий відсортований рядок: ", sorted("qwerty"))
# У Python можна виконати сортування списку на місці за допомогою методу sort():
a = [10,3,4,1,9]
print("первинний список: ", a)
# print("відсортований список: ", sorted(a)) # [1, 3, 4, 9, 10]
# b = ["-10","30","hello", "True", "4", "1","Світ", "9"]
# print("відсортований список: ", sorted(b)) # 
print(a.sort()) # [1, 3, 4, 9, 10]
print(a)  
# # Якщо елементи списку є вкладеними списками, то сортування буде відбуватися за першими елементами вкладених списків, в разі матриці - за першим стовпцем:
a = [[12,101],[2,200],[18,99]]
a.sort() # [[2, 200], [12, 101], [18, 99]]
print(a) 
# # Якщо потрібно відсортувати не по першому стовпцю, можна вказати аргумент у вигляді функції.
def sort_col(i):
  return i[1]
a.sort(key=sort_col) # [[2, 200], [12, 101], [18, 99]]
print(a)
a.sort(key=lambda x: x[0]) # Можна використовувати lambda-функцію

a.sort(key=lambda x: x[1]) # [[18, 99], [12, 101], [2, 200]]
print(a)
a = [(1, 2), (4, 1), (9, 10), (13, -3)]
a.sort(key=lambda x: x[1])  # [(13, -3), (4, 1), (1, 2), (9, 10)]
print(a)


# animals = ['ferret', 'vole', 'dog', 'cat', 'gecko']

# print(sorted(animals))

# print(sorted(animals, key=len))

# print(sorted(animals, key=len, reverse=True))


# def revers_len(s):
#     return -len(s)

# print(sorted(animals, key=revers_len))

# a = [10, 3, 4, 1, 9]
# a.sort()
# print(a)

b = [
    [12, 101],
    [2, 200],
    [8, 99]
]
b.sort()
print(b)

# def sort_col(i):
#     return i[1]

# b.sort(key=sort_col)
# print(b)

# b.sort(key=lambda x: x[0])
# print(b)

# b.sort(key=lambda x: x[1])
# print(b)