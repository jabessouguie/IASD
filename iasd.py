# the time interval in which the evaluation and new assignments are done
t = 5

# a set of medical doctors in the urgency room
# 1st component is the efficiency, 2nd is if they occupied or not
MD = [[1, False], [0.5, False]]

# r a set of bracelet colors (patient labels)
PL = [[10, 15], [20, 10][40, 5]]

# the set of patients
# 1st component : the time the patient was waiting before the scheduling
# 2nd component : indicates the label associated to the patient p
# 3rd component : if the patient is with a doctor or not
# 4th component : how much time the patient has actually being waiting before scheduling
# 5th component :

P = [[0, 0o1, False, 0, 0], [15, 0o3, False, 0, 0], [0, 0o2, False, 0, 0], [5, 0o1, False, 0, 0],
     {10, 0o3, False, 0, 0}, [15, 0o3, False, 0, 0]]

# List of assignment doctor/patient

A = [[0, None], [1, None]]

# Defining a state
state = [MD, PL, P, A]


def assign_patient_to_doctor(s, n, m):
    """

    :param s: current state
    :param n: number of the doctor to whom we wants to assign a patient
    :param m: number of the patient to whom we'll assign a doctor
    :return: a new state s1 where the patient m is assigned to the doctor n
    """
    s[0] = MD
    s[1] = PL
    s[2] = P
    s[3] = A

    # Say the doctor n is now taking care of the patient m
    A[n][1] = m

    # The doctor n is now busy
    MD[n][1] = True

    # The patient m is now busy
    P[m][2] = True

    # Creating a new state updated
    s1 = [MD, PL, P, A]
    return s1


def make_patient_leave(s, n, m):
    """

    :param s: the current s
    :param n: number of the doctor n we want to take the patient out
    :param m: number of the patient m we want to take out
    :return: a new state s1 where the doctor n has no patient
    """
    s[0] = MD
    s[1] = PL
    s[2] = P
    s[3] = A
    # Doctor n isn't busy anymore
    MD[n][1] = False

    # Patient m isn't taken in charge anymore
    P[m][2] = False

    # Doctor n isn't taking care of anyone right now
    A[n][1] = None

    # Updating the state
    s1 = [MD, PL, P, A]
    return s1


def time_wait(s):
    """

    :param s: the current state
    :return: a new state where the time every patient has been waiting is now updated
    """
    s[0] = MD
    s[1] = PL
    s[2] = P
    s[3] = A
    # In all the patient
    for p in P:
        if not p[2]:
            p[3] += 5
    s1 = [MD, PL, P, A]
    return s1


def consultation_time(s):
    """

    :param s: the current state s
    :return: a new state where the time every patient has been in consultation is now updated
    """
    s[0] = MD
    s[1] = PL
    s[2] = P
    for p in P:
        if p[2]:
            p[3] += 5
    s1 = [MD, PL, P, A]
    return s1


def find_doctor(s, m):
    """

    :param s: the current state
    :param m: number of the patient
    :return: number of the doctor taking care of the patient m
    """
    s[3] = A
    for x in range(len(A)):
        if A[x][1] == m:
            return A[x][0]


def replace_one_by_another(s, m1, m2):
    """

    :param s: the current state
    :param m1: the patient we want to make leave
    :param m2: the patient we want to assign a doctor
    :return: a new state where the patient m1 has no doctor and the patient m2 has no doctor
    """
    n = find_doctor(s, m1)
    s1 = make_patient_leave(s, n, m1)
    s2 = assign_patient_to_doctor(s1, n, m2)
    return s2


def actions(s):
    """

    :param s: the current state
    :return: a list (or a generator) of operators applicable to state s;
    """
    l = []
    s[0] = MD
    s[1] = PL
    s[2] = P
    s[3] = A
    for m in MD:
        if m[1]:
            for p in P:
                if p[2]:
                    l.append("assign_patient_to_doctor(s,n,m)")


def result():
    """

    :return: Returns the state resulting from applying action a to state s
    """


def goal_test():
    """

    :return: True if state s is a goal state, and False otherwise;
    """


def path_cost(c, s1, a, s2):
    """

    :param s2:
    :param c: cost of s1 :param s1: the initial state :param a: the action to apply :param s2: the state we will
    reach :return: Returns the path cost of state s2, reached from state s1 by applying action a, knowing that the
    path cost of s1 is c
    """


def load(f):
    """

    :param f: file object
    :return: Loads a problem from a (opened) file object f
    """


def save(f, s):
    """

    :param f: a file f where to find the solution
    :param s: state f
    :return: Saves a solution state s to a (opened) file object f
    """


def search():
    """

    :return: True or False, indicating whether it was possible or not to find a solution
    """


def cost(path):
    """

    :param path: the path to consider
    :return: the  cost of  path
    """
    c = 0
    for c in path():
        c += path_cost(c, )
