# Функція filter(function, iterable) застосовує функцію-аргумент function до кожного значення  у вхідному ітераторі iterable 
# та повертає новий ітератор з тими елементами, які пройшли фільтрацію. 
# Перший аргумент function має бути об’єктом функції - потрібно передати функцію, не викликаючи її за допомогою пари круглих дужок, Ця функція повертає True або False відповідно до умови і відіграє роль функції фільтрації, оскільки надає критерії для фільтрації небажаних значень з вхідного ітерованого елемента та збереження значень у результуючому ітерованому об’єкті. Термін небажані значення відноситься до тих значень, які мають значення false, коли filter() обробляє їх.
# Другий аргумент може містити будь-який ітерований об’єкт,  такий як список, кортеж або набір. Він також може містити об’єкти генератора та ітератора.  filter() приймає лише одну ітерацію. Результатом є об’єкт фільтра, що є ітератором, який видає значення на вимогу,  сприяючи стратегії ледачого оцінювання. Функція не змінює вихідний iterable.

# filter(function, iterable)
numbers = [-2, -1, 0, 1, 2]
# Щоб створити предикат, можна використовувати лямбда або функцію користувача:

# Виклик filter() відфільтровує від’ємні числа та 0.
positive_numbers = filter(lambda n: n > 0, numbers)
print(positive_numbers) # <filter object at 0x7f3632683610>
print(list(positive_numbers)) # [1, 2]

# Визначення функції is_positive(), яка отримує число як аргумент і повертає True, якщо число більше за 0, в іншому випадку повертає False.
def is_positive(n):
  return n > 0

# Виклик filter() застосовує is_positive() до кожного значення в списку,відфільтровуючи від’ємні числа.
# Оскільки filter() повертає ітератор, потрібно викликати list(), щоб створити остаточний список.
print(list(filter(is_positive, numbers))) # [1, 2]


# потрібно обробити список цілих чисел і створити новий список, що містить парні числа.
numbers = [1, 3, 10, 45, 6, 50]

def extract_even(numbers):
    even_numbers = []
    for n in numbers:
        if n % 2 == 0: # Умовний оператор відіграє роль фільтра, та перевіряє кожне парне число.
            even_numbers.append(n)  
    return even_numbers

# print(extract_even(numbers))


# ви можете виконати ті самі обчислення без використання явного циклу:



# def is_even(number):
#     return number % 2 == 0  # Filtering condition
# list(filter(is_even, numbers)) # [10, 6, 50]
# print(list(filter(is_even, numbers)))
# list(filter(is_even, range(10))) # filter() повертає ітератор, необхідно викликати list, який створює список.
# print(list(filter(is_even, range(100))))
# print(list(filter(lambda x: x % 2 == 0, range(10)))) # [0, 2, 4, 6, 8]
# print([x for x in range(11) if x%2 == 0]) # Реалізація, що використовує генератор списку

# filter() дозволяє фільтрувати елементи з iterable-об'єкта на основі оцінки заданої функції:
# filter(<f>, <iterable>) застосовує функцію <f> до кожного елемента <iterable> і повертає ітератор, що дає всі елементи, для яких результат функції <f> є правдивим. І навпаки, відфільтровує всі елементи, для яких результат функції <f> є хибним.
def greater_than_100(x):
  return x > 100
list(filter(greater_than_100, [1, 111, 2, 222, 3, 333])) # [111, 222, 333]
list(filter(lambda x: x > 100, [1, 111, 2, 222, 3, 333])) # функцію можна замінити лямбда-виразом
animals = ["cat", "Cat", "CAT", "dog", "Dog", "DOG", "emu", "Emu", "EMU"]
print(list(filter(lambda x: 'o' in x, ['cat', 'dog', 'cow']))) # ['dog', 'cow']
def all_caps(s):
  return s.isupper()
list(filter(all_caps, animals)) # ['CAT', 'DOG', 'EMU']
list(filter(lambda s: s.isupper(), animals)) # ['CAT', 'DOG', 'EMU']
print(list(filter(lambda x: x % 3 == 0, [2, 18, 9, 22, 17, 24, 8, 12, 27]))) # список усіх елементів кратних 3.

print(list(filter(lambda x: x > 50 , range(100))))

animals = ['ferret', 'vole', 'dog', 'cat', 'gecko']

print(list(filter(lambda x: 'o' in x, animals)))
# Функція is_prime() приймає ціле число як аргумент і повертає True, якщо число є простим, і False в іншому випадку.
import math

def is_prime(n):
  if n <= 1:
      return False
  for i in range(2, int(math.sqrt(n)) + 1):
      if n % i == 0:
          return False
  return True
# виклик filter() повертає всі прості числа в діапазоні від 1 до 50.
print(list(filter(is_prime, range(1, 51)))) # [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

import math

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

print(list(filter(is_prime, range(1, 51))))

import statistics as st

data = [10, 8, 10, 8, 2, 7, 9, 1, 45, 9, 6, 9, 100]
# Середнє значення є досить популярним вимірюванням центральної тенденції та часто є першим підходом до аналізу набору даних. Середнє значення дає швидке уявлення про центр або розташування даних.

# У деяких випадках середнє значення не є достатньо хорошим показником  центральної тенденції для даної вибірки. Викиди є одним із елементів, які впливають на точність середнього значення. Викиди – це точки даних, які суттєво відрізняються від інших спостережень у вибірці чи сукупності. Крім цього, у статистиці для них немає єдиного математичного визначення.

# Однак у нормально розподілених вибірках викиди часто визначаються як точки даних, які лежать більше ніж на два стандартних відхилення від вибіркового середнього. Тепер припустімо, що у вас є нормально розподілена вибірка з деякими викидами, які впливають на середню точність.  Викиди - це неправильні дані. Можна використовувати кілька функцій із модуля статистики разом із filter() для очищення даних.

mean = st.mean(data)

# The mean before removing outliers
print(mean)
# (function) def mean(data: Iterable[_NumberT@mean]) -> _NumberT@mean
# Return the sample arithmetic mean of data.

# >>> mean([1, 2, 3, 4, 4])
# 2.8
# >>> from fractions import Fraction as F
# >>> mean([F(3, 7), F(1, 21), F(5, 3), F(1, 3)])
# Fraction(13, 21)
# >>> from decimal import Decimal as D
# >>> mean([D("0.5"), D("0.75"), D("0.625"), D("0.375")])
# Decimal('0.5625')

stdev = st.stdev(data)
# Return the square root of the sample variance.
# See variance for arguments and other details.
# >>> stdev([1.5, 2.5, 2.5, 2.75, 3.25, 4.75])
# 1.0810874155219827
low = mean - 2 * stdev
high = mean + 2 * stdev 
clean_data = list(filter(lambda x: low <= x <= high, data))
print(clean_data)
print(st.mean(clean_data))


sample = [10, 8, 10, 8, 2, 7, 9, 3, 34, 9, 5, 9, 25]

mean = st.mean(sample) # The mean before removing outliers
print(mean) # 10.692307692307692

stdev = st.stdev(sample)
low = mean - 2 * stdev
high = mean + 2 * stdev

clean_sample = list(filter(lambda x: low <= x <= high, sample))
print(clean_sample) # [10, 8, 10, 8, 2, 7, 9, 3, 9, 5, 9, 25]
# The mean after removing outliers
print(st.mean(clean_sample)) # 8.75 
# dev(data)
low = mean - 2*stdev
high = mean + 2*stdev

real_data = list(filter(lambda x: low <= x <= high, data))
print(real_data)
print(st.mean(real_data))



# Знайти паліндромні слова у списку рядків. Слово-паліндром читається як назад, так і вперед. Типовими прикладами є «мадам»
def is_palindrome(word):
 # змінюєте оригінальне слово і зберігає його в reversed_word.
 reversed_word = "".join(reversed(word))
 # повертає результат порівняння обох слів на рівність.
 return word.lower() == reversed_word.lower()

is_palindrome("Racecar") # True
is_palindrome("Python") # False

# Ось як ви можете використовувати filter() для виконання важкої роботи:
words = ("filter", "Ana", "hello", "world", "madam", "racecar")
list(filter(is_palindrome, words))# ['Ana', 'madam', 'racecar']
