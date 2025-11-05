# Модуль Itertools містить спеціальні функції для управління ітерованими об'єктами.

import itertools

# Зокрема є можливість продублювати генератор, з'єднати два генератори, згрупувати значення вкладених списків тощо

# Для прикладу, можливі результати кінних гонок з 4 кіньми:

horses = [1, 2, 3, 4]
races = itertools.permutations(horses)
print(races)
# <itertools.permutations 0xb754f1dc="" at="" object="">
print(list(itertools.permutations(horses)))



