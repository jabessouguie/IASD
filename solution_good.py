#from search.py import Problem, Node, depth_first_tree_search
from itertools import permutations
from copy import deepcopy

# state is defined as:
#
#	[0] - patientList of structure [patientID, currentWaitingTime, maxWaitingTime, consultationTimeLeft]
#	[1] - doctorList of structure [doctorID, efficiency, patient1, ..., patientn]
#	[2] - doneTime
class Problem:
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value. Hill Climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError


# ______________________________________________________________________________


class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # We want for a queue of nodes in breadth_first_graph_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        return hash(self.state)


# ______________________________________________________________________________
def depth_first_tree_search(problem):
    """
    [Figure 3.7]
    Search the deepest nodes in the search tree first.
    Search through the successors of a problem to find a goal.
    The argument frontier should be an empty queue.
    Repeats infinitely in case of loops.
    """

    frontier = [Node(problem.initial)]  # Stack

    while frontier:
        node = frontier.pop()
        problem.debugfile(node.state)
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))

    return None

class PMDAProblem(Problem):
        
        timeStep = 5
	
        def __init__(self, initial, goal=[]):
            self.initial = initial
            self.goal = goal

        def actions(self, state):
                # we have only one possible action: to fill all doctors with patients
                # since we can not touch the algorithm it's simpler to return the permutation of patients and apply them to result()
                # since we can not check for validity of nodes during execution, we must check during this step to only provide valid permutations
                validPermutations = []
                for perm in permutations(state[0], len(state[1])):
                    self.debug.write(str(perm) + '\n')
                    for i in range(len(state[0])):
                        nthpatient = state[0][i]
                        if(nthpatient[0] != perm[0][0] and nthpatient[0] != perm[1][0]):
                            if nthpatient[1]+self.timeStep > nthpatient[2]:
                                break
                    else:
                        validPermutations.append(deepcopy(perm))
                return iter(validPermutations)

        def result(self, state, action):
            
                # keep our previous state clean
                newState = deepcopy(state)
                # we get a certain permutation of patients to add to our doctors, sequentially
                # for each element of our permutation (a patient element) we add it's ID to the n-th doctor
                # we also decrement the consultation time by timeStep*efficiency and decrement waiting time by timeStep
                # decrementing waiting time by timeStep allows us to easily add waiting time to patients not in office without checking
                for index, p in enumerate(action):
                        # add patient to doctor
                        doctor = newState[1][index]
                        doctor.append(p[0])
                        # lower remaining consultation time
                        # check if the patient will be done with consultation
                        # if patient is done, add his time to state[2] to avoid recomputing
                        # else we lower total waiting time to simplify incrementing only on patients waiting           
                        for i in range(len(newState[0])):
                            nthpatient = newState[0][i]
                            if nthpatient[0] == p[0]:
                                nthpatient[3] -= self.timeStep*doctor[1]
                                nthpatient[1] -= self.timeStep
                                if(nthpatient[3]<=0):
                                    newState[2] += p[1]**2
                                    newState[0].pop(i)
                                    break
                        
                # add timeStep to all patients in list
                for p in newState[0]:
                        p[1] += self.timeStep
                return newState
		

        def goal_test(self, state):
            return state[0] == self.goal

        def path_cost(self, c, state1, action, state2):
                return 0

        def value(self, state):
                # iterate patients and adds waiting room cost to the cost of patients already gone
                total = 0
                for p in state[0]:
                        total += p[1]**2
                return state[2] + total

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
                                    doctorList.append( [prelist[1], float(prelist[2])])
                            elif prelist[0] == 'PL':
                                    labelList.append( (prelist[1], int(prelist[2]), int(prelist[3])) )
                            elif prelist[0] == 'P':
                                    # labelList[int(prelist[3])][1] - this mess is actually very simple
                                    # grab the correct label from the already filled in list - labelList[n]
                                    # using the correct label assigned to our patient - int(prelist[3]) <--- note the int so it becomes the index
                                    # and then we select the consultation time form that label - LabelList[n][2]
                                    patientList.append( [prelist[1], int(prelist[2]), labelList[int(prelist[3])-1][1], float(labelList[int(prelist[3])-1][2])])
                                    
            state = [patientList, doctorList, 0]

            self.initial = state
				
            return
		
        def save(self, fh):
                for d in self.state[1]:
                        d.pop(1)
                        fh.write(' '.join(map(str, d)) + '\n')
                return
		
        def search(self):
            self.debug = open('debug.txt', 'w')
            self.state = self.initial
            finalNode = depth_first_tree_search(self)
            self.debug.close()
            if finalNode is not None:
                self.state = finalNode.state
                return True
            else:
                return False
            
            
        def debugfile(self, state):

            for d in state[1]:
                self.debug.write(' '.join(map(str, d)) + '\n')
            self.debug.write('---\n')
            for d in state[0]:
                self.debug.write(' '.join(map(str, d)) + '\n')
            self.debug.write('/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n')
			

