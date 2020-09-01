#!/usr/bin/env python3

import sys
import os
import csv

class Lab:
    def __init__(self):
        self.room = ''
        self.hour = ''
        self.group = ''
        self.day = ''

class Person:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        #Days as keys, Lab object as values
        self.labs = {}
    
    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.name + ' has email ' + self.email

    def get_lab_by_group(self, group):
        for lab_list in self.labs.values():
            for lab in lab_list:
                if lab.group == group:
                    return lab
    
    def display_labs(self):
        for day, labs in self.labs.items():
            print(day + ': ', end='')
            for lab in labs:
                print(lab.room + ':' + lab.hour + ' ,', end='')
            print()
    
 

NAME = "Nume"
ABREV = "Abreviere"
EMAIL = "E-mail"
HEADER_START = 'Luni'
TABLE_WIDTH = 6
TABLE_HEIGHT = 7

def get_team_info(team_table):
    '''Returns a member dictionary with name as keys and Person object as values
    and a dictionary with abreviations as keys and names as values'''
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

def skip_to_table(csv_reader, word):
    '''Skips anything unless it finds the specified word'''
    index = -1
    for header in csv_reader:
        if word in header:
            index = header.index(word) - 1
            break
    return index, header

def get_table(csv_reader, start_index, header):
    '''Returns a table in the csv_reader file with the first collumn at start_index'''
    end_index = start_index + TABLE_WIDTH
    
    #Add the trimmed header of the table
    table = [header[start_index:end_index]]
    height = 1

    #Select the rest of the rows of the table
    for row in csv_reader:
        if height < TABLE_HEIGHT :
            table.append(row[start_index:end_index])
            height += 1
        else:
            break

    return table

def map_abreviation_name(members, table, abrev_map, file_write, room):
    '''Uses an dicitonary of abreviation:names to map the allocation table and writes it in an CSV file
    adds labs to each person that teaches it'''
    writer = csv.writer(file_write)
    writer.writerow(table[0])

    for row_idx in range(1,TABLE_HEIGHT):
        new_row = [table[row_idx][0]]
        for col_idx in range(1,TABLE_WIDTH):
            abrev = table[row_idx][col_idx]
            if abrev in abrev_map:
                #Creating a new lab(without the group name)
                day = table[0][col_idx]

                lab = Lab()
                lab.room = room
                lab.hour = table[row_idx][0]
                lab.day = day

                #Map the abrevs to names
                name = abrev_map[abrev]
                new_row.append(name)

                #Add the lab to the coresponding person
                if not day in members[name].labs:
                    members[name].labs[day] = []
                
                members[name].labs[day].append(lab)
            else:
                new_row.append(abrev)
        writer.writerow(new_row)

def add_group_to_lab(members, day, hour, group, room):
    '''Completes the group for an registered lab'''
    for person in members.values():
        if day in person.labs:
            for lab in person.labs[day]:
                if lab.hour == hour and lab.room == room:
                    lab.group = group
                    return person.name
            
def add_groups(series, members, table, room):
    '''Complete the groups to registered labs and completes the dictionary with
    series name as keys and lists with tuples of format (<subroup>,<teacher_name>) '''
    for row_idx in range(1,TABLE_HEIGHT):
        for col_idx in range(1,TABLE_WIDTH):
            group = table[row_idx][col_idx]
            day = table[0][col_idx]
            hour = table[row_idx][0]

            if not group == '':
                name = add_group_to_lab(members, day, hour, group, room)
                if not name == None:
                    #Hardcoded indexes for ???<group>* format
                    series[group[3:5]].append((group, name))
                else:
                    print("This lab doesn't have a person associated")


def process_schedule(schedule_file, members, rooms):
    '''Returns a dictionary with series name as keys and lists with tuples of format (<subroup>,<teacher_name>) '''
    csv_file = open(schedule_file)
    reader = csv.reader(csv_file)
    #Manually added series
    series = {'AC':[],'CA':[], 'CB':[], 'CC':[], 'CD':[]}
    for room in rooms:
        index, header = skip_to_table(reader, HEADER_START)
        table = get_table(reader, index, header)
        add_groups(series, members,table, room)
    csv_file.close()
    return series

def process_allocation(allocation_file, members, rooms, abrev_map):
    '''Register labs to teachers and creates the allocation CSV'''
    csv_file = open(allocation_file)
    reader = csv.reader(csv_file)
    writer = open('ALOCARE_FINALA.csv','w')
    #Skip the first table
    skip_to_table(reader, HEADER_START)
    for room in rooms:
        index, header = skip_to_table(reader, HEADER_START)
        table = get_table(reader, index, header)
        writer.write(room + '\n')
        map_abreviation_name(members,table,abrev_map,writer, room)
        writer.write('\n')
    csv_file.close()
    writer.close()

def sort_series(element):
    '''Sort helper to sort by the first element of a tuple'''
    return element[0]

def sample_ocw_schedule(members, series):
    header = '^'.join(['Grupa', 'Zi', 'Ora', 'Sala', 'Asistent'])
    header = '^' + header + '^'
    writer = open('schedule_ocw', 'w')
    for _list in series.values():
        writer.write(header + '\n')
        _list.sort(key=sort_series)
        for group, name in _list:
            lab = members[name].get_lab_by_group(group)
            row = '|'.join([group, lab.day, lab.hour, lab.room, name])
            writer.write('|' + row + '|\n')

def sort_memmbers(person):
    return person.name

def sample_mail_list(members):
    writer = open('mail_list', 'w')
    _list = list(members.values())
    _list.sort(key=sort_memmbers)
    writer.write('==== Asistenti ====\n')
    for person in _list:
        if len(person.labs) > 0 :
            writer.write('   * [[ {} | {}]]\n'.format(person.email, person.name))
    writer.write('==== Colaboratori ====\n')
    for person in _list:
        if len(person.labs) == 0 :
            writer.write('   * [[ {} | {}]]\n'.format(person.email, person.name))
    writer.close()

if len(sys.argv) != 4 :
    print("Usage: " + sys.argv[0] + " TEAM_CSV ALOCARE_CSV ORAR_CSV")
    sys.exit(1)

rooms = ['EG306', 'EG106']


members, mapping_table = get_team_info(sys.argv[1])
process_allocation(sys.argv[2],members, rooms, mapping_table)
series = process_schedule(sys.argv[3], members, rooms)

sample_ocw_schedule(members, series)
sample_mail_list(members)