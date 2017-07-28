# -*- coding: utf-8 -*-
import csv
import json

api_dict = {}
filename = 'datayes_table_list.csv'

counter = 0
with open(filename, 'r') as f:
    reader = csv.reader(f)
    header = reader.next()
    for row in reader:
        name = row[1].split('.')[1]
        time = row[-1]
        if time not in api_dict:
            api_dict[time] = []
        api_dict[time].append(name)
        counter += 1

filename = 'api_dict.json'
with open(filename, 'w') as f:
    json.dump(api_dict, f)

print api_dict
print counter