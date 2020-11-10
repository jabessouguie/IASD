import search

class PMDAProblem(search.class):
	
	# timeStep definition for algorithm tuning
	# outside of project scope, good practice anyway
	timeStep = 5
	
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
        self.goal = []
		
	def actions(self, state):
		
		return (addPatienttoDoctor, removePatientfromDoctor)
		
		
	def goal_test(self, state):

        return self.patientList == self.goal
		
		
	def path_cost(self, c, state1, action, state2):	
		
		for
		
		return c + 1
	
	# this is the recursive function that digs for the answer
	# state must include patient list information, we have to send it into the next step
	def search(self, state, patientList):
		
		# we need to make sure we don't pollute this data
		nextState = copy.deepcopy(state)
		patientList = copy.deepcopy(self.patientList)
		
		# Rhis is our priority list for patients
		# Right now we are strictly enforcing FIFO-like behaviour. 
		# The longest waiting time goes first even if we have patient/doctor shuffling
		patientHeuristic = []
		# we simply look through patients and add the tuple (patientID, totalWaitingTime) to our queue
		# then quickly organize the priority list by decreasing waiting time
		for p in self.patientList:
			patientHeuristic.append((self.patientList[0], self.labelList[int(self.patientList[2])][1]))
		patientHeuristic.sort(key=lambda x: x[1], reverse=true)
		
		# our new state can be defined as previous stateStep+1, where each step is 5min
		# path cost can be defined as the cost of the target state. Initialized at 0 until state is defined
		newState = [0, state[1] + 1]
		for d in state[2:]:
			for p in patientList:
				if p[0] == patientHeuristic[0]:
					newState.append(list(d).append(p[0])
					p[3] -= 5*grabDoctor(self, d[0])[1]
					p[4] = true
		
		
	
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