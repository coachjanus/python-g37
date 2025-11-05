# Створення власного генератора у Python


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
#         gen1.throw(ValueError("We don't like large paliandromes"))
#     gen1.send(10 ** d)


for i in gen1:
    d = len(str(i))
    if d == 5:
        gen1.close()
    gen1.send(10 ** d)