Usage: 
-
./process_infrastructure.py <team_csv_path> <allocation_csv_path> <schedule_csv_path>

Input:
-
* team_csv: A csv file containing the team members with at least name, abbreviation(acronym) 
and e-mail address in the header;
* allocation_csv: A csv file containing tables of allocation that have abbreviation(acronym) as cell values.
The script skips the first table;
* schedule_csv: A csv file containing tables of the scheduled groups with the same format as the allocation_csv and 
groups as cell values.

Constraints:
 * allocation_csv and schedule_csv must have the same table format;
 * allocation_csv must have one table more than schedule_csv unless further changes are made;
 * allocation_csv and schedule_csv must have the tables in the same order.
 
Output:
-
* alocare_finala.csv: A csv file containing the tables from allocation_csv that has names (accordingly to team_csv 
name-abbreviation mapping) as cell values;
* schedule_ocw: A file which contains tables for each series with the header [Grupă, Zi, Oră, Sală, Asistent];
* mail_list: A file that contains two mail lists(teacher assistants and collaborators).

Configurations:
- 
* Macros: 
    * NAME -> stores the name of corresponding to the name field in team_csv, default value : "Nume";
    * ABREV -> stores the name of corresponding to the abbreviation field in team_csv, default value : "Abreviere";
    * EMAIL -> stores the name corresponding to the email field in team_csv, default value : "E-mail";
    * HEADER_START stores the name corresponding to the second field in the tables contained in allocation_csv and 
    schedule_csv, default value : 'Luni';
    * TABLE_WIDTH -> stores the number of fields in the tables contained in allocation_csv and 
    schedule_csv ,default value : 6;
    * TABLE_HEIGHT -> stores the number of entries(including the header) in the tables contained in allocation_csv and 
    schedule_csv, default value : 7;
    * TEACHERS_NUMBER -> stores the number of persons that won't appear in the mailing list(the first TEACHERS_NUMBER in
     the team_csv, which are usually the teachers), default value : 4;
    * ROOMS -> stores the rooms in which the labs take place, they should be in the same order as the tables in the
     allocation_csv and schedule_csv, default value : ['EG306', 'EG106'];
* Other changes:
    * sample_mail_list(): the printing format can be changed at need;
    * sample_ocw_schedule(): the printing format can be changed at need;
    * process_schedule(): the series dictionary has to be manually adapted; 
    * add_groups(): the groups must be parsed to match the series dictionary keys added in process_schedule().

Requirements:
	python3
	gnumeric
	ssconvert

