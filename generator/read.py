import csv

with open("data.csv", newline='') as myFile:
    reader = csv.reader(myFile)
    
    for row in reader:
        print(row)