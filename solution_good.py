from search.py import Problem, Node, depth_first_tree_search
from itertools import permutations

# state is defined as:
#
#	[0] - patientList of structure [patientID, currentWaitingTime, maxWaitingTime, consultationTimeLeft]
#	[1] - doctorList of structure [doctorID, efficiency, patient1, ..., patientn]
#	[2] - doneTime


class PMDAProblem(search.Problem):
        
        timeStep = 5
	
        def __init__(self, initial, goal=[]):
            self.initial = initial
            self.goal = goal

        def actions(self, state):
                # we have only one possible action: to fill all doctors with patients
                # since we can not touch the algorithm it's simpler to return the permutation of patients and apply them to result()
                # since we can not check for validity of nodes during execution, we must check during this step to only provide valid permutations
                validPermutations = permutations(state[0], len(state[1]))
                for per in validPermutations:
                        for p in state[0]:
                                if p not in per :
                                        if i[1]+self.timeStep > i[2]:
                                                permutations.remove(p)
                                                break
                                                        
                                
                return iter(validPermutations)

        def result(self, state, action):
                # we get a certain permutation of patients to add to our doctors, sequentially
                # for each element of our permutation (a patient element) we add it's ID to the n-th doctor
                # we also decrement the consultation time by timeStep*efficiency and decrement waiting time by timeStep
                # decrementing waiting time by timeStep allows us to easily add waiting time to patients not in office without checking
                for index, p in action:
                        # add patient to doctor
                        doctor = state[1][index]
                        doctor.append(p[0])
                        # lower remaining consultation time
                        p[3] -= timeStep*doctor[1]
                        # check if the patient will be done with consultation
                        # if patient is done, add his time to state[2] to avoid recomputing
                        # else we lower total waiting time to simplify incrementing only on patients waiting
                        if(p[3]<=0):
                                state[2] += p[1]**2
                                state[0].remove(p)
                        else:
                                p[2] -= self.timeStep
                        
                # add timeStep to all patients in list
                for p in state[0]:
                        p[1] += timeStep
		
		

        def goal_test(self, state):
                if isinstance(self.goal, list):
                        return is_in(state, self.goal)
                else:
                        return state[0] == self.goal

        def path_cost(self, c, state1, action, state2):
                return 0

        def value(self, state):
                # iterate patients and adds waiting room cost to the cost of patients already gone
                total = 0
                for p in state2[0]:
                        total += p[1]**2
                return state2[2] + total

        def load(self, fh):
                doctorList = []
                labelList = []
                patientList = []

                for l in fh:
                        prelist = l.split(" ")
                        if len(prelist) > 1:
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
                                        patientList.append( (prelist[1], prelist[2], labelList[int(prelist[3])][1], labelList[int(prelist[3])][2]) )

                state = [patientList, doctorList, 0]

                self.initial = state
				
				return
		
        def save(self, fh):
                for d in self.state[1]:
                        d.pop(1)
                        fh.write(' '.join(map(str, d)))
                return
		
		def search(self):
			finalState = depth_first_tree_search(self)
			if  finalState is not None:
				self.state = finalState
				return True
			else:
				return False
			

