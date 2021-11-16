import random
import math
import copy
from vsearch import *

# Algorithm 5 - Exercises week 37
def simulatedAnnealing(initialSolution):
    T = 100000000000  # Temperature - Fixed value
    r = 0.995    # Pick value between 0.8 - 0.99
    C = initialSolution
    curr_best = copy.deepcopy(initialSolution)
    tried = 0
    print_counter = 0

    while (T > 1):
        if print_counter % 1000 == 0:
            print('T: ', T)
            print_counter = 0
        CP = neighbourhood(C)
        prob = random.uniform(0,1)
        if (AccProbability(Cost(C), Cost(CP), T) > prob):
            tried += 1
            C = CP
            feasible = isSolution(C)
            if (feasible and Cost(curr_best) > Cost(C)):    # New solution is feasible and better than current
                curr_best = copy.deepcopy(C)
            elif (feasible and not isSolution(curr_best)):  # New solution is feasible while current is not feasible
                curr_best = copy.deepcopy(C)
            elif (not feasible and not isSolution(curr_best) and Cost(curr_best) > Cost(C)):    # both new and current are not feasible but new is better than current
                curr_best = copy.deepcopy(C)

        T = T * r
        print_counter += 1

    print("Tried " + str(tried) + " different solutions.")
    return curr_best

# Find 'nearby' solution
def neighbourhood (msgs,vertices):
    prob = random.uniform(0,1)
    # pick a random msg2route object
    randomMsg = random.choice(msgs)
    # pick a random index between 0 and the length of the route array of that
    # msg2route object -2 (as randint is not inclusive second argument and it
    # makes no sense to find a new route from the second to last node as it will
    # pick the same route again, as it can see the destination from that node).
    randomEdgeC = random.randint(0,len(randomMsg.Route)-2)
    randomEdge = randomMsg.Route[randomEdgeC]
    print("Picked message " + str(randomMsg.Msg.Name))
    print("Picked index " + str(randomEdgeC))

    if (prob > 0.5):
        # slices the route array such that we only include up to edge before the
        # randomly chosen edge 
        randomMsg.Route = randomMsg.Route[:randomEdgeC]

        print("Performing search from " + str(randomEdge.Source) + " to " +
              str(randomMsg.Msg.Destination))

        # rebuild visited and stack
        visited = []
        stack = []
        for r in randomMsg.Route:
            visited.append(r.Destination)
            stack.append(r.Destination)

        search(randomEdge.Source,visited,stack,randomMsg,vertices)
    else:
        e_len = len(vertices[randomEdge.Source].Egress)
        rand = random.randint(1,e_len+1)
        print("Changing queue of edge " + str(randomEdge.Id) + " from " +
              str(randomEdge.Queue) + " to " + str(rand))
        ind = vertices[randomEdge.Source].Egress.index(randomEdge)
        vertices[randomEdge.Source].Egress[ind].Queue = rand



# Probability function which will allow inferior solutions. The lower T, the
# less likelyhood of choosing inferior solutions.
def AccProbability(costCurrent, costNeighbour, T):
    if (costCurrent > costNeighbour):
        return 1.1
    else:
        return math.exp( (costCurrent - costNeighbour) / T)

# Penalty function
def Cost(chips):
    # Weights
    nonFeasibleWeight = 100000
    taskCountWeight = 50
    orderWeight = 250
    cost = 0

    for chip in chips:
        for coreID in chip.Cores:
            taskCount = 0
            curr_core = chip.Cores[coreID]

            prevTaskDeadline = 0
            prevTaskWCET = 0
            numUnordered = 0

            for t in curr_core.TasksList:
                # Penalize if tasks are unordered according to deadline in core
                if int(t.Deadline) < prevTaskDeadline and prevTaskDeadline != 0:
                    cost += 1 + numUnordered * orderWeight
                    numUnordered += 1

                # If they have the same deadline, penalize for unordered
                # according to WCET
                elif int(t.Deadline) == prevTaskDeadline:
                    if int(t.WCET) > prevTaskWCET:
                        cost += 1 + numUnordered * orderWeight
                        numUnordered += 1

                prevTaskDeadline = int(t.Deadline)
                prevTaskWCET = int(t.WCET)

                taskCount += 1
                # The more tasks on a core, the bigger the penalty
                cost += taskCount * taskCountWeight
                # Prioritize having slow tasks on fast cores
                cost += float(curr_core.WCETFactor) * float(t.WCET)

    # If neighbour is not a solution, add massive penalty
    feasible = isSolution(chips)
    if (not feasible):
        cost += nonFeasibleWeight
    return cost


def Cost_new(msgs):    
    # # Weights
    # nonFeasibleWeight = 100000
    # taskCountWeight = 50
    # orderWeight = 250
    cost = 0

    # # for chip in chips:
    #     for coreID in chip.Cores:
    #         taskCount = 0
    #         curr_core = chip.Cores[coreID]

    #         prevTaskDeadline = 0
    #         prevTaskWCET = 0
    #         numUnordered = 0

    #         for t in curr_core.TasksList:
    #             # Penalize if tasks are unordered according to deadline in core
    #             if int(t.Deadline) < prevTaskDeadline and prevTaskDeadline != 0:
    #                 cost += 1 + numUnordered * orderWeight
    #                 numUnordered += 1

    #             # If they have the same deadline, penalize for unordered
    #             # according to WCET
    #             elif int(t.Deadline) == prevTaskDeadline:
    #                 if int(t.WCET) > prevTaskWCET:
    #                     cost += 1 + numUnordered * orderWeight
    #                     numUnordered += 1

    #             prevTaskDeadline = int(t.Deadline)
    #             prevTaskWCET = int(t.WCET)

    #             taskCount += 1
    #             # The more tasks on a core, the bigger the penalty
    #             cost += taskCount * taskCountWeight
    #             # Prioritize having slow tasks on fast cores
    #             cost += float(curr_core.WCETFactor) * float(t.WCET)

    # # If neighbour is not a solution, add massive penalty
    feasible = isSolution(msgs)
    if (not feasible):
        cost += nonFeasibleWeight
    return cost





# Checks if solution is scheduble 
def isSolution(solution, lax=[]):
    tl = 0
    feasible = True
    
    for m in solution:
        print ('ddl: ', m.Msg.Deadline, ' vs E2E: ', m.E2E )
        if ( int (m.E2E) > int(m.Msg.Deadline) ):
            feasible = False
    
    return feasible

