# -*- coding: utf-8 -*-
import csv
import json

filename = 'datayes_table_list.csv'
new_filename = 'table_list_v3.csv'

def generate_dict(my_file):
    counter = 0
    api_dict = {}
    with open(my_file, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        header = reader.next()
        for row in reader:
            name = row[1].split('.')[1]
            time = row[3]
            if time not in api_dict:
                api_dict[time] = []
            api_dict[time].append(name)
            counter += 1
    return api_dict

out1 = 'set_v1.json'
out2 = 'set_v3.json'

set_v1 = set()
with open(filename, 'r') as f:
    reader = csv.reader(f)
    header = reader.next()
    for row in reader:
        name = row[1].split('.')[1]
        set_v1.add(name)

set_v3 = set()
with open(new_filename, 'r') as f:
    reader = csv.reader(f, delimiter=',')
    header = reader.next()
    for row in reader:
        name = row[1].split('.')[1]
        set_v3.add(name)

with open(out1, 'w') as f:
    json.dump(list(set_v1), f)

with open(out2, 'w') as f:
    json.dump(list(set_v3), f)

print set_v3 - set_v1