# Program title: Flattening the Curve - classes 
# Team number: 2
# Individual author: Leia Wang, leiawang@usc.edu


class Group:
	def __init__(self, ID, count, m, prob):
		""" Initializes group object """
		self.id = ID # group ID: a unique combination of upper-case letters and digits
		self.headcount = count # number of members belonging to the group
		self.members = m # list of members
		self.status = 'open' # open: members can meet and infect each other, close: members cannot meet
		self.prob_infect = prob # probability that an infected individual may infect another member of the group, if the group is open

	def close(self):
		self.status = 'close'

	def open(self):
		self.status = 'open'

	def is_infected(self):
		""" Returns true if a group has an infected member that can start infecting others in the group """
		for i in self.members:
			if i.status == 'infected' and i.days_infected > 0:
				return True

class Person():
	def __init__(self, person_id):
		self.person_id = person_id # person ID
		self.days_infected = 0 # the number of days the person has been infected
		self.status = 'susceptible' # person can be either susceptible, infected, hospitalized, or recovered 

	def infected(self):
		self.status = 'infected'

	def hospitalized(self):
		self.status = 'hospitalized'

	def recovered(self):
		self.status = 'recovered'

	def new_simulation(self):
		""" Reset people object for new simulation """
		self.days_infected = 0
		self.status = 'susceptible'

	def update_days_infected(self):
		self.days_infected += 1
