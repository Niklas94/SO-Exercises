import random
import math
import copy
from vsearch import *
import time
from typing import List

# Set to True to receive timing info on calculations during Simulated Annealing,
# False to mute
timing = True

# Set modulo for which i'th iterations to print information in
print_mod = 50

# Generates unique string ids for 3 given solutions. These Ids are an
# amalgamation of the link ids and queue numbers used in the routes.
def genId(C):
    id = ""
    for ro in C:
        id += ro.Id
    return id

# Algorithm 5 - Exercises week 37
def simulatedAnnealing(initialSolution,vertices,edges):
    T = 10000000            # Temperature - Fixed value
    r = 0.99                # Pick value between 0.8 - 0.99
    C = initialSolution
    curr_best = copy.deepcopy(initialSolution)
    tried = 0
    print_counter = 0
    # Dictionary to cache feasability of solutions. The key is the unique id for
    # the solution, the value is the feasability associated
    isSolutions = {}
    # Dictionary to cache costs of solutions. The key is the unique id for the
    # solution, the value is the cost associated
    costs = {}
    hcl = calculateHyperCycleLength(initialSolution)

    initFeasible, init_mb = isSolution(initialSolution,hcl,edges)
    for ro in initialSolution:
        ro.CalculateE2E()
    costBefore = Cost(initialSolution, init_mb, edges)
    totalTime = time.time()

    # Solely used for timing in debugging
    solutionTotalTime   = 0.0
    costTotalTime       = 0.0
    checksTotalTime     = 0.0
    updateTotalTime     = 0.0

    while (T > 1):
        if print_counter % print_mod == 0:
            print('T: {temp:.2f}'.format(temp = T))
        CP = neighbourhood(C,vertices)
        prob = random.uniform(0,1)

        # Generate unique IDs for the 3 solutions
        cp_id = genId(CP)
        cb_id = genId(curr_best)
        c_id = genId(C)

        # Debugging purposes
        sUpdate = time.time()

        # Update E2Es
        for ro in CP:
            ro.CalculateE2E()
        for ro in C:
            ro.CalculateE2E()
        for ro in curr_best:
            ro.CalculateE2E()

        # Debugging purposes
        if timing:
            ti = time.time() - sUpdate
            updateTotalTime += ti

        # Debugging purposes
        sSol = time.time()

        # If a key,value pair of either of the 3 solutions that are looked at in
        # this iteration does not exist in the isSolutions dict, create it
        if isSolutions.get(cp_id) == None:
            isSolutions[cp_id] = isSolution(CP,hcl,edges)
        if isSolutions.get(cb_id) == None:
            isSolutions[cb_id] = isSolution(curr_best,hcl,edges)
        if isSolutions.get(c_id) == None:
            isSolutions[c_id] = isSolution(C,hcl,edges)
        sol_cb,cb_mb = isSolutions[cb_id]
        sol_cp,cp_mb = isSolutions[cp_id]
        _, c_mb = isSolutions[c_id]

        # Debugging purposes
        if timing:
            ti = time.time() - sSol
            solutionTotalTime += ti

        # Debugging purposes
        sCost = time.time()

        if costs.get(cp_id) == None:
            costs[cp_id] = Cost(CP,cp_mb,edges)
        if costs.get(cb_id) == None:
            costs[cb_id] = Cost(curr_best,cb_mb,edges)
        if costs.get(c_id) == None:
            costs[c_id] = Cost(C,c_mb,edges)
        cost_c = costs[c_id]
        cost_cb = costs[cb_id]
        cost_cp = costs[cp_id]

        # Debugging purposes
        if timing:
            ti = time.time() - sCost
            costTotalTime += ti

        # Debugging purposes
        sChecks = time.time()

        if (AccProbability(cost_c, cost_cp, T) > prob):
            tried += 1
            C = CP
            if (sol_cp and cost_cb > cost_cp):    # New solution is feasible and better than current
                curr_best = copy.deepcopy(C)
            elif (sol_cp and not sol_cb):  # New solution is feasible while current is not feasible
                curr_best = copy.deepcopy(C)
            elif (not sol_cp and not sol_cb and cost_cb >
                  cost_cp):    # both new and current are not feasible but new is better than current
                curr_best = copy.deepcopy(C)

        # Debugging purposes
        if timing:
            ti = time.time() - sChecks
            checksTotalTime += ti

        T = T * r

        # Debugging purposes
        if timing:
            if print_counter % print_mod == 0:
                fs = "Feasability \t{pm:d} \t{time:.7f}s \t{ttime:.7f}s \t{perc:.4f}%"
                ct = "Cost \t\t{pm:d} \t{time:.7f}s \t{ttime:.7f}s \t{perc:.4f}%"
                cs = "Checks \t\t{pm:d} \t{time:.7f}s \t{ttime:.7f}s \t{perc:.4f}%"
                up = "Update E2E \t{pm:d} \t{time:.7f}s \t{ttime:.7f}s \t{perc:.4f}%"
                end = "{t:.7f}s per iteration of simulated annealing."

                total = solutionTotalTime + costTotalTime + checksTotalTime + updateTotalTime

                print("Type \t\tAmount \tAverage time \tTotal time \tPercentage")
                print("------------------------------------------------------------------")
                print(fs.format(pm = print_mod, time = solutionTotalTime /
                                print_mod, ttime = solutionTotalTime, perc =
                                (solutionTotalTime / total) * 100))
                print(ct.format(pm = print_mod, time = costTotalTime /
                                print_mod, ttime = costTotalTime, perc =
                                (costTotalTime / total) * 100))
                print(cs.format(pm = print_mod, time = checksTotalTime /
                                print_mod, ttime = checksTotalTime, perc =
                                (checksTotalTime / total) * 100))
                print(up.format(pm = print_mod, time = updateTotalTime /
                                print_mod, ttime = updateTotalTime, perc =
                                (updateTotalTime / total) * 100))
                print(end.format(t = total / print_mod))
                print()

                solutionTotalTime   = 0.0
                costTotalTime       = 0.0
                checksTotalTime     = 0.0
                updateTotalTime     = 0.0

        print_counter += 1

    print("Done in {time:.2f}s.".format(time = (time.time()-totalTime)))
    print("Tried {t:d} different solutions.".format(t = tried))

    foundFeasible, found_mb = isSolution(curr_best,hcl,edges)
    costAfter = Cost(curr_best, found_mb, edges)
    print("Cost before: {c:.2f}.".format(c = costBefore))
    print("Cost after: {c:.2f}.".format(c = costAfter))

    print("Initial solution was feasible: " + str(initFeasible))
    print("Found solution was feasible: " + str(foundFeasible))

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
def Cost(solution : List[Route], maxBandwidths : List[int], E : List[Edge]):
    tE2E = 0
    # Omega is the average bandwidth used overall
    omega = 0
    for r in solution:
        tE2E += r.E2E
    for b in maxBandwidths:
        omega += b
    omega /= len(E)
    return tE2E + omega

# Checks if solution is scheduble 
def isSolution(solution : List[Route], C, edges):
    ret = True
    for r in solution:
        if not r.MeetsDeadline():
            ret = False
            break
    linkCap, max_bandwidths = linkCapacityConstraint(solution,C,edges)
    
    return ((ret and linkCap), max_bandwidths)

def calculateHyperCycleLength(solution: List[Route]):

    # LCM (least common multiple) over all messages/flows

    # Source for calculating LCM: https://www.includehelp.com/python/find-the-lcm-of-the-array-elements.aspx
    lcm = int(solution[0].Msg.Period)

    for i in range(1, len(solution)):
        a_i = int(solution[i].Msg.Period)
        lcm = (lcm*a_i)//math.gcd(lcm, a_i)

    return math.ceil(lcm / 12)

# Check that for every cycle, no link is transmitting more data than their bandwidth
def linkCapacityConstraint(solution: List[Route], C : int, E : List[Edge]):

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
    ret = True
    max_bandwidths = [0] * len(E)
    for cycle in range(1,C+1):
        B_link_cs = [0] * len(E)
        for route in solution:
            alphas = [0] * len(E)
            prev_alph = 0
            for la in route.LinkAssignments:
                indexOfCurrentLink = E.index(la.Link)
                prev_alph += la.QueueNumber
                alphas[indexOfCurrentLink] += prev_alph
                prev_alph = prev_alph + la.Link.InducedDelay
            for e in range(0,len(E)):
                # If specific edge hasn't been touched (the alpha value
                # associated with it is 0), we do not want to calculate arrival
                # pattern for it
                if (alphas[e] == 0):
                    ap = 0
                else:
                    ap = route.Msg.ArrivalPattern(cycle - alphas[e])
                B_link_cs[e] += ap
        for e in range(0,len(E)):
            if B_link_cs[e] > max_bandwidths[e]:
                max_bandwidths[e] = B_link_cs[e]
            if (B_link_cs[e] > E[e].Capacity):
                # As we need to calculate max bandwidths we cannot just return
                # False directly here, but have to iterate through the rest of
                # the edges first
                ret = False

    for i in range(0,len(E)):
        max_bandwidths[i] = (max_bandwidths[i]//E[i].Capacity)*1000

    return (ret, max_bandwidths)

        # OLD SOLUTION
        # for link in E:
        #     B_link_c = 0
        #     for route in solution:
        #         alpha = 0
        #         for la in route.LinkAssignments:
        #             if la.Link != link:
        #                 continue
        #             alpha += la.Link.InducedDelay + la.QueueNumber
        #             print("A " + str(alpha))

        #         B_link_c += route.Msg.ArrivalPattern(cycle - alpha)


        #     print(B_link_c)
        #     if (B_link_c > link.Capacity):
        #         print("Link " + str(link) + " goes over the bandwith limit in cycle " + str(cycle))
        #         return False
        # return True

