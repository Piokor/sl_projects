import csv
import time

def rjust_my(string, length, character=" "):
    just_len = length - len(string) if length - len(string) < 0 else 0 
    return character * just_len + string

def load_data():
    result = []
    with open('data.csv') as data_file:
        reader = csv.reader(data_file, delimiter=",")
        for row in reader:
            result.append((row[0], int(row[1]), row[2]))
    return result

data = load_data()

start = time.time()
for x in data:
    rjust_my(x[0], x[1], x[2])
print(time.time() - start)

start = time.time()
for x in data:
    x[0].rjust(x[1], x[2])
print(time.time() - start)
