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

# cProfile.run('sum([i*2 for i in range(10000)])')
# invokes the cProfile module to profile the execution of the string statement. cProfile.run takes a statement (here a string) and executes it under the profiler, then prints profiling statistics to stdout (or writes them to a file if you pass the optional filename). The wrapper you showed delegates to the Profile implementation, so the profiler records function call counts, total time spent in each function, and cumulative times before printing the usual table (ncalls, tottime, percall, cumtime, etc.).

# The profiled statement constructs a list of 10,000 integers via a list comprehension and then sums them:

# The list comprehension produces elements 

# O(n) memory (n=10000). The bulk of CPU time will be in Python-level loop operations and list construction.
# Gotchas and small improvements

# Passing the code as a string causes cProfile to exec the string; profiling a Python function with Profile.runcall or Profile.runctx (or cProfile.runctx) is often clearer and less error-prone.
# Avoid building the full list if you don’t need it; use a generator expression to reduce peak memory:

# ```python# Use a generator to avoid allocating the listcProfile.run('sum(i*2 for i in range(10000))')

# - For profiling a callable directly:```python```python# Profile a function call (no string exec)pr = cProfile.Profile()pr.runcall(my_function, arg1, arg2)pr.print_stats()

# - If you want to save stats for later inspection with pstats or snakeviz:```python```pythoncProfile.run('sum([i*2 for i in range(10000)])', filename='out.prof')

# For microbenchmarks, consider timeit instead of the full profiler; for algorithmic profiling across modules, keep the profiled region small so the output is easier to interpret.
# ```python
# # Use a generator to avoid allocating the list
# cProfile.run('sum(i*2 for i in range(10000))')

# - For profiling a callable directly:
# ```python
# ```python
# # Profile a function call (no string exec)
# pr = cProfile.Profile()
# pr.runcall(my_function, arg1, arg2)
# pr.print_stats()
# - If you want to save stats for later inspection with pstats or snakeviz:
# ```python
# ```python
# cProfile.run('sum([i*2 for i in range(10000)])', filename='out.prof')
# For microbenchmarks, consider timeit instead of the full profiler; for algorithmic profiling across modules, keep the profiled region small so the output is easier to interpret.
# cProfile.run('sum([i*2 for i in range(10000)])')

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