import sys

my_generator = (x*x for x in range(1000))

print(sys.getsizeof(my_generator))

# for i in my_generator:
#     print(i)
    
# for i in my_generator:
#     print(i)
    
my_list = [x*x for x in range(1000)]
print(sys.getsizeof(my_list))

# for i in my_list:
#     print(i)
    
# for i in my_list:
#     print(i)
    
# print(my_list)

# print(my_generator)

import cProfile

cProfile.run('sum([i*2 for i in range(10000)])')

cProfile.run('sum((i*2 for i in range(10000)))')

import itertools

horses = [1,2,3,4]
races = itertools.permutations(horses)
# print(races)

# print(list(itertools.permutations(horses)))


def createGenerator():
    my_list = range(10)
    for i in my_list:
        yield i*i
        
my_generator = createGenerator()

# for i in my_generator:
#     print(i)
    
def infinite_sequence():
    n = 0
    while True:
        yield n
        n += 1
        
# for i in infinite_sequence():
#     print(i, end=" ")

gen = infinite_sequence()

print(next(gen))
print(next(gen))
print(next(gen))

def is_paliandrome(n):
    if n // 10 == 0:
        return False
    tmp = n
    reversed_n = 0
    
    while tmp != 0:
        reversed_n = (reversed_n * 10) + tmp % 10
        tmp = tmp // 10
        
    if n == reversed_n:
        return True
    else:
        return False
    

def infinite_paliandromes():
    n = 0
    while True:
        if is_paliandrome(n):
            i = (yield n)
            if i is not None:
                n = i
        n += 1

gen1 = infinite_paliandromes()

# for i in gen1:
#     d = len(str(i))
#     gen1.send(10 ** d)
    


# for i in gen1:
#     d = len(str(i))
#     if d == 5:
#         gen1.throw(ValueError("We don't like large pa;iandromes"))
#     gen1.send(10 ** d)


for i in gen1:
    d = len(str(i))
    if d == 5:
        gen1.close()
    gen1.send(10 ** d)