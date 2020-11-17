import copy
import 

class PMDAProblem(search.class):
	
	# timeStep definition for algorithm tuning
	# outside of project scope, good practice anyway
	timeStep = 5
	
	# our goal is to have an empty list of patients
	# patients are only removed from the list when consultationTimeLeft == 0
	goal = []
	
	# Lists of tuples
	# Doctor list is composed of ( doctorID, efficiency )
	doctorList = []
	# Label list is composed of ( labelID, maximumWait, consultationTime )
	labelList = []
	# Patient list is composed of (patientID, currentWaitingTime, labelID, consultationTimeLeft, isBusy )
	# isBusy is a boolean to help during cost calculations
	patientList = []

	
	# state is a tuple!
	# state( cost, timeInstant, MD0, MD1, MD2, MD3, ..., MDn )
	# MDn = ( MD , ID, patient, patient, ... , lastPatient)
	# timeInstant - defined in pdf as 5min
	state = ()
	
	# our problem loads the initial data from a file
	# initial state depends on how many doctors we have, it's not required or advised
	def __init__(self, initial=None, goal=None):
		
		load(input("Select file to open:\n"))
			
		#Initial state:
		# (0, 0, MD0, ... , MDn)
		#Doctors at state 0:
		# ( ID )
		initial = [0, 0]
		for d in doctorList:
			initial.append(d[0])		
		self.state = tuple(initial)
		
		
	def actions(self, state):
		
		return (addPatienttoDoctor, removePatientfromDoctor)
		
		
	def goal_test(self, state):

        return self.patientList == self.goal
		
	
	# path cost is defined by adding the waiting time of all patients still in the room
	# we consider that patients being treated are not in the room, thus not counting to cost
	def path_cost(self, patientList):	
		
		cost = 0
		for p in patientList:
			if p[4]:
				cost += p[1]**2
		
		return cost
	
	# this is the recursive function that digs for the answer
	# state must include patient list information, we have to send it into the next step
	def search(self, state, patientList):
		
		
		
		# ------------> when we return here for next node, this is where the loop goes!
		# search recursive algorithm:
		# 0> check if we reached goal
		# 1> organize patients by waiting time
		# 2> extract 'n' patients, where 'n' is number of doctors
		# 	2a> (investigate possibility of keeping patient with doctor)
		# 3> organize patients by consultation time
		# 4> assign first combination of patients to doctors in decreasing order of efficiency
		# 5> compute cost into expected state
		# 6> send current state into search() algorithm for next step
		
	
		# This is our priority list for patients
		# Right now we are strictly enforcing FIFO-like behaviour. 
		# The longest waiting time goes first even if we have patient/doctor shuffling
		# We convert the patientlist into a list of lists for processing
		patientList = copy.deepcopy(self.patientList)
		for p in patientList:
			p = list(p)
			
		# we simply look through patients and quickly organize the priority list by decreasing current waiting time
		# this metric should be solid enough, no need to do combinatorial magic with patients, simply chose next in line in worst case scenario
		patientList.sort(key=lambda x: x[1], reverse=true)
		
		
		# Cycle through doctors in our hospital and assign a patient to each
		# patients are defined as busy and their consultation time left is decremented by 5min * doctor efficiency
		doctorBuffer = []
		i=0
		for d in state[2:]:
			doctorBuffer.append(list(d).append(patientList[i][0])
			patientList[i][3] -= 5*grabDoctor(self, d[0])[1]
			patientList[i][4] = true
			i++
			
		# We have our patients assigned to doctors, we can now calculate the pathCost of this next pathCost
		newState = (path_cost(patientList), state[1]+1
		
		
	
	def value(self, state):
		pass
	
	def grabDoctor(self, docID):
		for d in self.doctorList:
			if d[0] == docID:
				return d
				
		print('Doctor not found with id \"' + docID + '\" when attempting to calculate efficiency')
		return 0
		
		
	def load(self, target):
		f = open(target, "r")
		doctorList = []
		labelList = []
		patientList = []

		for l in f:
			prelist = l.split(" ")
			prelist[-1] = prelist[-1].split('\n')[0]
			if prelist[0] == 'MD':
				# doctor - (ID, efficiency)
				doctorList.append( (prelist[1], prelist[2]) )
			elif prelist[0] == 'PL':
				labelList.append( (prelist[1], prelist[2], prelist[3]) )
			elif prelist[0] == 'P':
				# labelList[int(prelist[3])][1] - this mess is actually very simple
				# grab the correct label from the already filled in list - labelList[n]
				# using the correct label assigned to our patient - int(prelist[3]) <--- note the int so it becomes the index
				# and then we select the consultation time form that label - LabelList[n][2]
				patientList.append( (prelist[1], prelist[2], prelist[3], labelList[int(prelist[3])][2], false) )
		
		self.doctorList = tempList[0]
		self.labelList = tempList[1]
		self.patientList = tempList[2]
		
		return
		
	def save(self):
		#TODO - WRITE THIS!
		return