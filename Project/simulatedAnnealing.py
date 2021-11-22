import random
import math
import copy
from vsearch import *
import time

# Generates unique string ids for 3 given solutions. These Ids are an
# amalgamation of the link ids and queue numbers used in the routes.
def genIds(C,CP,CB):
    c_id = ""
    cp_id = ""
    cb_id = ""
    for ro in C:
        c_id += ro.Id
    for ro in CP:
        cp_id += ro.Id
    for ro in CB:
        cb_id += ro.Id
    return (c_id, cp_id, cb_id)

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
    costs = {}
    hcl = calculateHyperCycleLength(initialSolution)

    while (T > 1):
        # if print_counter % 1000 == 0:
        print('T: ', T)
            # print_counter = 0
        # neigh_start_time = time.time()
        CP = neighbourhood(C,vertices)
        # print("Neighbourhood function took " + str(time.time() -
        #                                            neigh_start_time))
        prob = random.uniform(0,1)
        # cost_start_time = time.time()
        c_id, cp_id, cb_id = genIds(C,CP,curr_best)
        # If a key,value pair of either of the 3 solutions that are looked at in
        # this iteration does not exist in the costs dict, create it
        if costs.get(c_id) == None:
            costs[c_id] = Cost(C,hcl,edges)
        if costs.get(cp_id) == None:
            costs[cp_id] = Cost(CP,hcl,edges)
        if costs.get(cb_id) == None:
            costs[cb_id] = Cost(curr_best,hcl,edges)
        cost_cb = costs[cb_id]
        cost_cp = costs[cp_id]
        if (AccProbability(costs.get(c_id), cost_cp, T) > prob):
            tried += 1
            C = CP
            feasible = isSolution(C)
            if (feasible and cost_cb > cost_cp):    # New solution is feasible and better than current
                curr_best = copy.deepcopy(C)
            elif (feasible and not isSolution(curr_best)):  # New solution is feasible while current is not feasible
                curr_best = copy.deepcopy(C)
            elif (not feasible and not isSolution(curr_best) and cost_cb >
                  cost_cp):    # both new and current are not feasible but new is better than current
                curr_best = copy.deepcopy(C)
        # print("Cost section took: " + str(time.time() - cost_start_time))

        T = T * r
        # print_counter += 1

    print("Tried " + str(tried) + " different solutions.")
    return curr_best

# Find 'nearby' solution
def neighbourhood (routes,vertices):
    prob = random.uniform(0,1)
    # pick a random route object
    randomRoute = random.choice(routes)
    # pick a random index between 0 and the length of the linkassignments array
    # of that route object -2 (as randint is not inclusive second argument and
    # it makes no sense to find a new route from the second to last node as it
    # will pick the same route again, as it can see the destination from that
    # node).
    randomLAC = random.randint(0,len(randomRoute.LinkAssignments)-1)
    randomLA = randomRoute.LinkAssignments[randomLAC]
    # print("Picked message " + str(randomRoute.Msg.Name))
    # print("Picked index " + str(randomLAC))
    # print("Id before: " + str(randomRoute.Id))

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
    # print("Id after: " + str(randomRoute.Id))
    return routes



# Probability function which will allow inferior solutions. The lower T, the
# less likelyhood of choosing inferior solutions.
def AccProbability(costCurrent, costNeighbour, T):
    if (costCurrent > costNeighbour):
        return 1.1
    else:
        return math.exp( (costCurrent - costNeighbour) / T)

# Penalty function
def Cost(solution, C, edges):
    tE2E = 0
    for r in solution:
        r.CalculateE2E()
        tE2E += r.E2E
    return tE2E + linkCapacityConstraint(solution, C, edges)

# Checks if solution is scheduble 
def isSolution(solution, lax=[]):
    # tl = 0
    # feasible = True
    # for route in solution:
    #     for coreID in chip.Cores:
    #         i = 0.0
    #         curr_core = chip.Cores[coreID]

    #         for t in curr_core.TasksList:
    #             # How long the task takes in this specific core
    #             responseTime = i + float(curr_core.WCETFactor) * float(t.WCET)
    #             i = responseTime
    #             tl += i

    #             if responseTime > float(t.Deadline):
    #                 feasible = False

    # # as lax is called by reference, we can use this total laxity score outside
    # # the function
    # lax.append(tl)
    return True

def calculateHyperCycleLength(solution: list[Route]):

    # LCM (least common multiple) over all messages/flows

    # Source for calculating LCM: https://www.includehelp.com/python/find-the-lcm-of-the-array-elements.aspx
    lcm = int(solution[0].Msg.Period)

    for i in range(1, len(solution)):
        lcm = math.ceil(lcm*int(solution[i].Msg.Period)//math.gcd(lcm, int(solution[i].Msg.Period)))    # Have to round up hypercycle

    return lcm

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


    # print('---------- Checking link capacity constraint ----------')
    penalty = 0
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
            # print("New route")
            alphas = [0] * len(E)
            for la in route.LinkAssignments:
                indexOfCurrentLink = E.index(la.Link)
                # print("Curr ind " + str(indexOfCurrentLink) + " adding " +
                #       str(la.Link.InducedDelay + la.QueueNumber))
                alphas[indexOfCurrentLink] += la.Link.InducedDelay + la.QueueNumber
                # print(alphas)
            for e in range(0,len(E)):
                # print("Cycle " + str(cycle) + " alpha " + str(alphas[e]))
                # print("Adding " + str(route.Msg.ArrivalPattern(cycle - alphas[e])) + " to " + str(e))
                B_link_cs[e] += route.Msg.ArrivalPattern(cycle - alphas[e])
                # print(B_link_cs)
        for e in range(0,len(E)):
            # print("B_link_value for " + str(e) + " is " + str(B_link_cs[e]) + " while capacity is " + str(E[e].Capacity))
            if (B_link_cs[e] > E[e].Capacity):
                # print("histo : " + str(histo[e]) + " cap " + str(E[e].Capacity))
                penalty += (B_link_cs[e] - E[e].Capacity)*500
                print("Over cap")

        # for link in E:
        #     B_link_c = 0
        #     for route in solution:
        #         alpha = 0
        #         for la in route.LinkAssignments:
        #             if la.Link != link:
        #                 continue
        #             alpha += la.Link.InducedDelay + la.QueueNumber

        #         B_link_c += route.Msg.ArrivalPattern(cycle - alpha)


        #     print(B_link_c)
        #     if (B_link_c > link.Capacity):
        #         penalty += (B_link_c - link.Capacity)*500
        #         print("Link " + str(link) + " goes over the bandwith limit in cycle " + str(cycle))

    return penalty
