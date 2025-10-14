# dict

# dict1 = {}

dict1 = {"name": "Tom Cat"}
# print(type(dict1))
# print(dict1)

# Creating a Dictionary with dict() method
Dict3 = dict({1: 'Cats', 2: 'For', 3:'Dogs'})
print(f"\nDictionary with the use of dict(): {Dict3}")
# Creating a Dictionary with each item as a Pair
Dict4 = dict([(1, 'Cats'), (2, 'Dogs')])
print(f"\nDictionary with each item as a pair: {Dict4}")

print(Dict4[1])
print(Dict4.items())
for k in Dict4.keys():
    print(k)
