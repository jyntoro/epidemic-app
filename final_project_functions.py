# Program title: Flattening the Curve - functions
# Team number: 2
# Individual author: Jayne Oentoro, oentoro@usc.edu

import numpy as np

# input data
n = 20	# number of people initially infected
k = 10 	# days to recovery
h = 7	# number of days until person needs to be hospitalized

def simulate(x, people_dict, groups):
	""" 
		Simulate one instance of an epidemic 
		
		INPUT ARGUMENTS
        x:  Minimum headcount of groups to close
        people_dict: Dictionary of Person objects initialized in main.py
        groups: List of Group objects initialized in main.py
        
    	RETURN VALUE
        The maximum demand of hospital beds 
	"""

	# refreshes all people object so they are all susceptible for a new simulation
	for member in people_dict.values():
		member.new_simulation() 

	# generate n randomly infected people
	random_list = [] 
	for i in range(n):
		temp_rand_person = np.random.choice(list(people_dict.values()))
		while temp_rand_person in random_list:
			temp_rand_person = np.random.choice(list(people_dict.values()))
		random_list.append(temp_rand_person)

	for person in random_list:
		rand_person = person
		for member in people_dict.values():
			if rand_person.person_id == member.person_id:
				member.infected()

	# Before simulation: 
	ni = n # total population in "infected" status (before simulation = n)
	beds_occupied = 0
	max_bed_demand = 0

	for group in groups:
		group.open() # reset all group objects so they are all open
		# counting the number of groups with a headcount of x or greater
		if group.headcount >= x:
			# close the groups with a headcount of x or greater
			group.close()

	# keep running simulation until epidemic ends (infected population = 0)
	# while ni != 0:
	while ni != 0:

		# beginning of the day
		infected_groups = [] # list of groups that has a member who is either infected or hospitalized
		for group in groups:
			for member in group.members:
				if member.status == 'infected' or member.status == 'hospitalized':
					infected_groups.append(group)
					break

		# update days infected and check for hospitalizations
		for member in people_dict.values():
			# if a member is infected or hospitalized, increment days infected 
			if member.status == 'infected' or member.status == 'hospitalized':
				member.update_days_infected()
			# if an infected member has reached the day to be hospitalized, close the group they are in
			if member.days_infected == h:
				member.hospitalized()
				group.close()
				beds_occupied += 1

		# check for infections within each open and infected group
		for group in infected_groups:
			for member in group.members:
				# if susceptible member is infected (only if the group has an infected member who is not hospitalized)
				if group.is_infected() and group.status == 'open' and member.status == 'susceptible':
					group_prob = group.prob_infect * group.headcount
					prob = np.random.rand() 
					if prob < group_prob:
						member.infected()
						ni += 1 # increment infected population

		# check for recoveries after a day of infections
		for member in people_dict.values():
			if member.days_infected == k:
				member.recovered()
				member.update_days_infected() # to make sure a recovered member in two groups is not accounted twice
				ni -= 1 # if a patient has recovered, it means they have moved from infection to recovered population
				beds_occupied -= 1 # add another bed to those available

		# updates the maximum bed demand 
		if max_bed_demand < beds_occupied:
			max_bed_demand = beds_occupied

	# return 
	return max_bed_demand

def monte_carlo(x, people_dict, groups, m=10):
	""" 
		Use Monte Carlo to get the average outcome of an stimulated epidemic

		INPUT ARGUMENTS
        x:  Minimum headcount of groups to close
        people_dict: Dictionary of Person objects initialized in main.py
        groups: List of Group objects initialized in main.py
        m:  Number of samples to simulate. 
        
    	RETURN VALUE
        The average maximum demand of hospital beds 
    """
	return np.mean([simulate(x, people_dict, groups) for i in range(m)])
