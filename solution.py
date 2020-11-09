import search

class PMDAProblem(search.class):
	
	# Lists of tuples
	# TODO - ADD COMMENT WITH INDIVIDUAL LIST EXPLANATION
	doctorList = []
	labelList = []
	patientList = []

	
	# state is a tuple!
	# TODO - ADD COMMENT WITH STATE EXPLANATION
	# state( cost, timeInstant, MD0, MD1, MD2, MD3, ..., MDn )
	# MDn = ( MD , ID, patient, patient, patient, ... , lastPatient)
	# timeInstant - defined in pdf as 5min
	state = ()
	
	
	def __init__(self, initial, goal=None):
		
		tempList = load(input("Select file to open:\n"))
		
		self.doctorList = tempList[0]
		self.labelList = tempList[1]
		self.patientList = tempList[2]
	
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
		
	def search(self, state):
		
		nextState = []
		patientHeuristic = []
		
		for p in self.patientList:
			patientHeuristic.append([self.patientList[0], self.labelList[int(self.patientList[2])][1])
		patientHeuristic.sort(key=lambda x: x[1], reverse=true)
		
		newState = [0, state[1] + 1]
		for d in state[2:]:
			for p in self.patientList:
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
		
		
	def load(target):
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
		
		return [doctorList, labelList, patientList]
		
	def save(self):
		#TODO - WRITE THIS!
		return