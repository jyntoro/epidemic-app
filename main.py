# Program title: Flattening the Curve - main
# Team number: 2
# Individual author: Neil Malayil, malayil@usc.edu

import csv
from final_project_classes import *
from final_project_functions import *

max_beds = 50 # maximum number of beds that can be occoupied for sick people in the hospital
filename = 'group_info_case_C.csv'

groups = [] # list of group objects
people_dict = {} # dictionary of EVERY person object, key: member_ID (integer), value: Person object
count_list = [] # list of headcount of each group

with open(filename, 'r') as csvfile:
	reader = csv.DictReader(csvfile)

	for row in reader:

		member_ID_list = [int(i) for i in row['members'].split(',')] # member (integer) list for each group
		member_list = [] # member (person object) list for each group

		for member_ID in member_ID_list: 
			if member_ID not in people_dict: # create person object if it's not yet in the people dictionary
				people_dict[member_ID] = Person(member_ID)
			member_list.append(people_dict[member_ID]) # add member to list of people objects

		count_list.append(int(row['headcount'])) # add the headcount of each group to the count list

		ID = row['group_ID'] # ID = each group's unique ID

		# create group object
		group = Group(ID, int(row['headcount']), member_list, float(row['prob']))
		groups.append(group) # add group object to list of group objects


max_x = 0
# max_bed_list = [] 

# min(count_list) = closing all groups
# max(count_list) + 1 = opening all groups

for x in range(min(count_list), max(count_list) + 2):
	max_bed_demand = monte_carlo(x, people_dict, groups)
	print('x:', x) 
	print('Max beds needed:', max_bed_demand)
	if max_bed_demand <= max_beds and x > max_x:
		max_x = x

print("Max x:", max_x)

# for bed in max_bed_list:
# 	print(bed)
