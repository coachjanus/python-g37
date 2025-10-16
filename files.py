# f = open("test.txt")
# f = open("test.txt", 'a')
# data = "\nthis is other test"
# f.write(data)
# f.close()

# f = open("test.txt", 'a')
# print(type(f))
# print(f.name)
# print(f.mode)
# print(f.closed)

# data = "this is some test"
# f.write(data)
# f.close()
# print(f.closed)

# try:
#     writer = open('data.txt', 'w')
#     print("file open for writing")
# except FileNotFoundError:
#     print("file not found error")
# finally:
#     if writer:
#         writer.close()
#     print("file closed")
    
# with open('data.txt', 'w') as f:
#     data = "Some data to be written to the file\n"
#     f.write(data)
#     data = "Other data to be written to the file\n"
#     f.write(data)
#     data = "And this data to be written to the file\n"
#     f.write(data)

# with open('data.txt') as f:
#     print(f.read())
    

# with open('data.txt') as f:
#     for l in f:
#         print(l)
        

def search(fl, w):
    with open(fl) as f:
        content = f.read()
        if w in content: 
            print(f"word {w} exists in the {fl}")
            
search('data.txt', 'Some')