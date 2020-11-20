from itertools import permutations
from copy import deepcopy
import search

class State():
    
    
    
    def __init__(self, plist, dlist, totalGone):
        self.plist = plist
        self.dlist = dlist
        self.totalGone = totalGone
        
    def __lt__(self, other):
        return self.totalGone < other.totalGone
        

class PMDAProblem(search.Problem):
        
        timeStep = 5
	
        def __init__(self, initial, goal=[]):
            self.initial = initial
            self.goal = goal

        def actions(self, state):
                # we have only one possible action: to fill all doctors with patients
                # since we can not touch the algorithm it's simpler to return the permutation of patients and apply them to result()
                # since we can not check for validity of nodes during execution, we must check during this step to only provide valid permutations
                validPermutations = []
                for perm in permutations(state.plist, len(state.dlist)):
                    for i in range(len(state.plist)):
                        nthpatient = state.plist[i]
                        if(nthpatient[0] != perm[0][0] and nthpatient[0] != perm[1][0]):
                            if nthpatient[1]+self.timeStep > nthpatient[2]:
                                break
                    else:
                        validPermutations.append(tuple((perm[0][0], perm[1][0])))
                return iter(validPermutations)

        def result(self, state, action):
            
            
            self.debugfile(state)
            # keep our previous state clean
            plist = list(state.plist)
            dlist = list(state.dlist)
            totalGone = deepcopy(state.totalGone)
            # we get a certain permutation of patients to add to our doctors, sequentially
            # for each element of our permutation (a patient element) we add it's ID to the n-th doctor
            # we also decrement the consultation time by timeStep*efficiency and decrement waiting time by timeStep
            # decrementing waiting time by timeStep allows us to easily add waiting time to patients not in office without checking
            #for index, d in enumerate(newState[1]):
            #doctorQueue.append(list(index, newState[1][1]))
            for index, p in enumerate(action):
                    
                    # add patient to doctor
                    #for d in doctorQueue:
                       # if()
                    #else:
                    
                    # turn doctor tuple into list, append patient, retuple
                    doctor = list(dlist[index])
                    doctor.append(p)
                    dlist[index] = tuple(doctor)
                    
                    # lower remaining consultation time
                    # check if the patient will be done with consultation
                    # if patient is done, add his time to state.totalGone to avoid recomputing
                    # else we lower total waiting time to simplify incrementing only on patients waiting
                    print('75---------------------------75')
                    print(action)
                    print(plist)
                    for i in range(len(plist)):
                        nthpatient = list(plist[i])
                        if nthpatient[0] == p:
                            print('ding')
                            nthpatient[3] -= self.timeStep*doctor[1]
                            nthpatient[1] -= self.timeStep
                            if(nthpatient[3]<=0):
                                totalGone += nthpatient[1]**2
                                plist.pop(i)
                                break
                        else:
                            print('noding')
                        plist[i] = tuple(nthpatient)
                    print(plist)
                    
            # add timeStep to all patients in list
            nlist = []
            for p in plist:
                    temp = list(p)
                    temp[1] += self.timeStep
                    nlist.append(tuple(temp))
            print(nlist)
            return State(nlist, dlist, totalGone)
		

        def goal_test(self, state):
            return state.plist == self.goal

        def path_cost(self, c, state1, action, state2):
                return 0

        def value(self, node):
                # iterate patients and adds waiting room cost to the cost of patients already gone
                total = 0
                for p in node.state.plist:
                        total += p[1]**2
                return node.state.totalGone + total

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
                                    doctorList.append( (prelist[1], float(prelist[2])))
                            elif prelist[0] == 'PL':
                                    labelList.append( (prelist[1], int(prelist[2]), int(prelist[3])) )
                            elif prelist[0] == 'P':
                                    # labelList[int(prelist[3])][1] - this mess is actually very simple
                                    # grab the correct label from the already filled in list - labelList[n]
                                    # using the correct label assigned to our patient - int(prelist[3]) <--- note the int so it becomes the index
                                    # and then we select the consultation time form that label - LabelList[n][2]
                                    patientList.append( (prelist[1], int(prelist[2]), labelList[int(prelist[3])-1][1], float(labelList[int(prelist[3])-1][2])))
                                    
            loaded = State(patientList, doctorList, 0)

            self.initial = loaded
				
            return loaded
		
        def save(self, fh):
                for d in self.state.dlist:
                        d.pop(1)
                        fh.write(' '.join(map(str, d)) + '\n')
                return
		
        def search(self):
            self.debug = open('debug.txt', 'w')
            self.state = self.initial
            finalNode = search.best_first_graph_search(self, self.value)
            self.debug.close()
            if finalNode is not None:
                self.state = finalNode.state
                return True
            else:
                return False
            
            
        def debugfile(self, state):

            for d in state.dlist:
                self.debug.write(' '.join(map(str, d)) + '\n')
            self.debug.write('---\n')
            for d in state.plist:
                self.debug.write(' '.join(map(str, d)) + '\n')
            self.debug.write('/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n')
			

