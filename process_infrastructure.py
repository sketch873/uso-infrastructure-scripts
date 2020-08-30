#!/usr/bin/env python3

import sys
import os
import csv

NAME = "Nume"
ABREV = "Abreviere"

def get_mapping_table(team_table):
    if not os.path.isfile(team_table):
        print('The path ' + team_table + ' does not coresspond to a file')
        sys.exit(-1)

    mapping_table = {}
    team_csv = open(team_table) 
    reader = csv.DictReader(team_csv)

    for row in reader:
        if row[ABREV] == "":
            print(row[NAME] + " has no acronym")
        elif not row[ABREV] in mapping_table:
            mapping_table[row[ABREV]] = row[NAME]
        else:
            print(row[NAME] + ' has the same acronym as ' + mapping_table[row[ABREV]])
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


if len(sys.argv) != 3 :
    print("Usage: " + sys.argv[0] + " TEAM_CSV ALOCARE_CSV")
    sys.exit(1)

mapping_table = get_mapping_table(sys.argv[1])
map_allocation(sys.argv[2],mapping_table)