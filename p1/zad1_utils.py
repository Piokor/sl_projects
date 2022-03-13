import csv
import time

def rjust_my(string, length, character=" "):
    just_len = length - len(string)
    return character * just_len + string

def load_data():
    result = []
    with open('data.csv') as data_file:
        reader = csv.reader(data_file, delimiter=",")
        first_row = True
        for row in reader:
            if first_row:
                first_row = False
                continue
            result.append((row[0], int(row[1]), row[2]))
    return result

def save_result(results, filename):
    with open(filename, 'w') as result_file:
        for result in results:
            result_file.write(result + "\n")

