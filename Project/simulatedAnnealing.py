import random
import math
import copy
from vsearch import *
import time

# Generates unique string ids for 3 given solutions. These Ids are an
# amalgamation of the link ids and queue numbers used in the routes.
def genId(C):
    id = ""
    for ro in C:
        id += ro.Id
    return id

# Algorithm 5 - Exercises week 37
def simulatedAnnealing(initialSolution,vertices,edges):
    T = 1000000   # Temperature - Fixed value
    r = 0.98    # Pick value between 0.8 - 0.99
    C = initialSolution
    curr_best = copy.deepcopy(initialSolution)
    tried = 0
    print_counter = 0
    # Dictionary to cache costs of solutions. The key is the unique id for the
    # solution, the value is the cost associated
    isSolutions = {}
    hcl = calculateHyperCycleLength(initialSolution)

    while (T > 1):
        if print_counter % 20 == 0:
            print('T: ', T)
            print_counter = 0
        CP = neighbourhood(C,vertices)
        prob = random.uniform(0,1)

        cp_id = genId(CP)
        cb_id = genId(curr_best)
        # If a key,value pair of either of the 2 solutions that are looked at in
        # this iteration does not exist in the isSolutions dict, create it
        if isSolutions.get(cp_id) == None:
            isSolutions[cp_id] = isSolution(CP,hcl,edges)
        if isSolutions.get(cb_id) == None:
            isSolutions[cb_id] = isSolution(curr_best,hcl,edges)
        sol_cb = isSolutions[cb_id]
        sol_cp = isSolutions[cp_id]

        if (AccProbability(Cost(C), Cost(CP), T) > prob):
            tried += 1
            C = CP
            if (sol_cb and Cost(curr_best) > Cost(C)):    # New solution is feasible and better than current
                curr_best = copy.deepcopy(C)
            elif (sol_cp and not sol_cb):  # New solution is feasible while current is not feasible
                curr_best = copy.deepcopy(C)
            elif (not sol_cp and not sol_cb and Cost(curr_best) >
                  Cost(C)):    # both new and current are not feasible but new is better than current
                curr_best = copy.deepcopy(C)

        T = T * r
        print_counter += 1

    print("Tried " + str(tried) + " different solutions.")
    return curr_best

# Find 'nearby' solution
def neighbourhood (routes,vertices):
    prob = random.uniform(0,1)
    randomRoute = random.choice(routes)
    randomLAC = random.randint(0,len(randomRoute.LinkAssignments)-1)
    randomLA = randomRoute.LinkAssignments[randomLAC]

    if (prob > 0.5):
        # slices the linkassignments array such that we only include up to
        # linkassignment before the randomly chosen linkassignment
        randomRoute.LinkAssignments = randomRoute.LinkAssignments[:randomLAC]
        # also slice id, such that a new can be build from here
        randomRoute.Id = randomRoute.Id[:randomLAC]

        # print("Performing search from " + str(randomLA.Link.Source) + " to " +
        #       str(randomRoute.Msg.Destination))

        # rebuild visited and stack
        visited = []
        stack = []
        for r in randomRoute.LinkAssignments:
            visited.append(r.Link.Destination)
            stack.append(r.Link.Destination)

        search(randomLA.Link.Source,visited,stack,randomRoute,vertices)
    else:
        rand = random.randint(1,3)
        # print("Changing queue of edge " + str(randomLA.Link.Id) + " from " +
        #       str(randomLA.QueueNumber) + " to " + str(rand))
        randomLA.QueueNumber = rand
        # as each link assignment contributes 2 numbers to the string (fst being
        # link id, snd being queue number) we have to multiply the index with 2
        # to get the correct link assignment in the id. +1 to target the queue
        # number and not link id.
        idQueueIndex = randomLAC*2+1
        # as you cannot change a specific character in string, one needs to
        # slice around the character and include the new one in the middle
        randomRoute.Id = randomRoute.Id[:idQueueIndex] + str(rand) + randomRoute.Id[idQueueIndex+1:]
    return routes



# Probability function which will allow inferior solutions. The lower T, the
# less likelyhood of choosing inferior solutions.
def AccProbability(costCurrent, costNeighbour, T):
    if (costCurrent > costNeighbour):
        return 1.1
    else:
        return math.exp( (costCurrent - costNeighbour) / T)

# Penalty function
def Cost(solution : list[Route]):
    tE2E = 0
    for r in solution:
        r.CalculateE2E()
        tE2E += r.E2E
    return tE2E

# Checks if solution is scheduble 
def isSolution(solution : list[Route], C, edges):
    ret = True
    for r in solution:
        if not r.MeetsDeadline():
            ret = False
            break
    return (ret and linkCapacityConstraint(solution,C,edges))

def calculateHyperCycleLength(solution: list[Route]):

    # LCM (least common multiple) over all messages/flows

    # Source for calculating LCM: https://www.includehelp.com/python/find-the-lcm-of-the-array-elements.aspx
    lcm = int(solution[0].Msg.Period)

    for i in range(1, len(solution)):
        a_i = int(solution[i].Msg.Period)
        lcm = (lcm*a_i)//math.gcd(lcm, a_i)

    return math.ceil(lcm / 12)

# Check that for every cycle, no link is transmitting more data than their bandwidth
def linkCapacityConstraint(solution: list[Route], C : int, E : list[Edge]):

    # Equation for this constraint

    # Hyper cycle       C
    # Cycle             c
    # Link              ε i,j
    # Set of links      Ε
    # Consumed bandwith of each link ε i,j in each cycle c noted as B c,j
    # arrival pattern function A(c) and the latency α

    # Other related notes

    # In each cycle we have an array of the B_link_c value for each edge.
    # B_link_cs[0] corresponds to the value of the first edge and so on. Each
    # route of the solution is then iterated and the alpha value of each edge
    # used in that route is calculated in the alphas array. These alpha values
    # can then be used to calculate the partial sum of the B_link_c for each
    # edge used in the route. When all routes have done this, B_link_cs should
    # include the correct B_link_c value for each edge based on all the messages
    # that used that edge. It can then be checked if this value is above the
    # capacity of the edge in a single cycle. This is then checked for each
    # cycle.
    for cycle in range(0,C):
        B_link_cs = [0] * len(E)
        for route in solution:
            alphas = [0] * len(E)
            prev_alph = 0
            for la in route.LinkAssignments:
                indexOfCurrentLink = E.index(la.Link)
                alphas[indexOfCurrentLink] += prev_alph
                prev_alph = prev_alph + la.Link.InducedDelay + la.QueueNumber
            for e in range(0,len(E)):
                ap = route.Msg.ArrivalPattern(cycle - alphas[e])
                B_link_cs[e] += ap
        for e in range(0,len(E)):
            if (B_link_cs[e] > 0):
                print("B_link_value for " + str(e) + " is " + str(B_link_cs[e]) + " while capacity is " + str(E[e].Capacity))
            if (B_link_cs[e] > E[e].Capacity):
                print("Over cap")
                return False

    return True

        # OLD SOLUTION
        # for link in E:
        #     B_link_c = 0
        #     for route in solution:
        #         alpha = 0
        #         for la in route.LinkAssignments:
        #             if la.Link != link:
        #                 continue
        #             alpha += la.Link.InducedDelay + la.QueueNumber

        #         B_link_c += route.Msg.ArrivalPattern(cycle - alpha)


        #     # print(B_link_c)
        #     if (B_link_c > link.Capacity):
        #         penalty += (B_link_c - link.Capacity)*500
        #         print("Link " + str(link) + " goes over the bandwith limit in cycle " + str(cycle))

