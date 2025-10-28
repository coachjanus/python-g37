
def reader(file):
    f = open(file)
    result = f.read().split("\n")
    return result

# gen1 = reader('some')
# count = 0
# for row in gen1:
#     count += 1
# print(count)

csv_gen = (row for row in open('some'))

def csv_reader():
    for row in open('some'):
        yield
        
import csv

data = [
    [1,2,3],
    ['foo', 'bar', 'baz']
]

# with open('data1.csv', 'w') as f:
#     writer1 = csv.writer(f)
#     writer1.writerows(data)


# with open('data1.csv', newline='\n') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         print(row)


file_name = 'data.csv'
lines = (line for line in open(file_name))

list_line = (s.rstrip().split(',') for s in lines)

cols = next(list_line)

company_dicts = (dict(zip(cols, data)) for data in list_line)

founding = (
    int(company_dict['raisedAmt'])
    for company_dict in company_dicts 
    if company_dict['round'] == 'a'
)

total_series_a = sum(founding)

print(f"Total series A: ${total_series_a}")


import pandas

df = pandas.read_csv('data.csv')

# print(df)

per_round = df.groupby("round")['raisedAmt'].sum()
print(per_round)


def fac(x):
    a = 1
    for i in range(1, x + 1):
        a *= i
        yield a

for x in fac(100):
    print(x, end=" ")
    
def fibo(n):
    if n in (0,1):
        return n
    return fibo(n-1) + fibo(n-2)

print([fibo(n) for n in range(10)])