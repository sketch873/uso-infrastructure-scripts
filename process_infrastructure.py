#!/usr/bin/env python3

import sys
import os
import csv

class Lab:
    def __init__(self):
        self.day = ''
        self.hour = ''
        self.group = ''

class Person:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        #Rooms as keys, Lab object as value
        self.labs = {}
    
    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.name + ' has email ' + self.email
 

NAME = "Nume"
ABREV = "Abreviere"
EMAIL = "E-mail"

def get_team_info(team_table):
    if not os.path.isfile(team_table):
        print('The path ' + team_table + ' does not coresspond to a file')
        sys.exit(-1)
    
    members = {}
    abrev_map = {}

    team_csv = open(team_table)
    reader = csv.DictReader(team_csv)

    for row in reader:
        if row[NAME] in members:
            print(row[NAME] + " has multiple entryes in table")
            continue

        members[row[NAME]] = Person(row[NAME], row[EMAIL])

        if row[ABREV] == '':
            print(row[NAME] + " has no abreviation")
        elif not row[ABREV] in abrev_map:
            abrev_map[row[ABREV]] = row[NAME]
        else:
            print(row[NAME] + ' has the same abreviation as ' + abrev_map[row[ABREV]])
            abrev_map[row[ABREV]] += ' | ' + row[NAME]

    team_csv.close()
    return members, abrev_map

def skip_to_table(csv_reader):
    index = -1
    for row in csv_reader:
        if 'Luni' in row:
            index = row.index('Luni') - 1
            break
    return index

def get_table(csv_reader, start_index):
    TABLE_WIDTH = 6
    TABLE_HEIGHT = 6
    end_index = start_index + TABLE_WIDTH
    
    table = []
    height = 0
    for row in csv_reader:
        if height < TABLE_HEIGHT :
            table.append(row[start_index:end_index])
            height += 1
        else:
            break

    return table

def get_mapping_table(team_table):
    if not os.path.isfile(team_table):
        print('The path ' + team_table + ' does not coresspond to a file')
        sys.exit(-1)

    mapping_table = {}
    team_csv = open(team_table) 
    reader = csv.DictReader(team_csv)

    for row in reader:
        if row[ABREV] == "":
            print(row[NAME] + " has no abreviation")
        elif not row[ABREV] in mapping_table:
            mapping_table[row[ABREV]] = row[NAME]
        else:
            print(row[NAME] + ' has the same abreviation as ' + mapping_table[row[ABREV]])
            mapping_table[row[ABREV]] += ' | ' + row[NAME]
    
    team_csv.close()
    return mapping_table

def map_allocation(allocation_table, mapping_table):
    if not os.path.isfile(allocation_table):
        print('The path ' + allocation_table + ' does not coresspond to a file')
        sys.exit(-1)
    
    allocation_csv = open(allocation_table)
    allocation_final = open('alocare_finala.csv','w')

    reader = csv.reader(allocation_csv)
    writer = csv.writer(allocation_final)

    for row in reader:
        new_row = []
        for cell in row:
            if cell in mapping_table:
                new_row.append(mapping_table[cell])
            else:
                new_row.append(cell)
        writer.writerow(new_row)
    
    allocation_csv.close()
    allocation_final.close()


if len(sys.argv) != 4 :
    print("Usage: " + sys.argv[0] + " TEAM_CSV ALOCARE_CSV ORAR_CSV")
    sys.exit(1)

rooms = ['EG306', 'EG106']


#test
f = open(sys.argv[3])
reader = csv.reader(f)

index = skip_to_table(reader)
t = get_table(reader, index)
print(t)
print('-' * 20)
index = skip_to_table(reader)
t = get_table(reader, index)
print(t)

#mapping_table = get_mapping_table(sys.argv[1])
#members, mapping_table = get_team_info(sys.argv[1])
#map_allocation(sys.argv[2],mapping_table)
#print(members)