import random
import math
import copy


# Algorithm 5 - Exercises week 37
def simulatedAnnealing(initialSolution):
    T = 1000000000  # Temperature - Fixed value
    r = 0.995    # Pick value between 0.8 - 0.99
    C = initialSolution
    curr_best = copy.deepcopy(initialSolution)
    tried = 0
    print_counter = 0

    while (T > 1):
        if print_counter % 1000 == 0:
            print('T equal: ', T)
            print_counter = 0
        CP = neighbourhood(C)
        prob = random.uniform(0,1)
        if (AccProbability(Cost(C), Cost(CP), T) > prob):
            # print("Curr best: " + str(Cost(curr_best)))
            # print("Picking " + str(Cost(CP)) + " over " + str(Cost(C)))
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
def neighbourhood (chips):
    c = copy.deepcopy(chips)

    for i in range (0,1):
        # find first random core
        tList = []
        while (len(tList) == 0):
            randomChip = random.choice(c)
            choice = list(randomChip.Cores.keys())
            CoreId = random.choice(choice)
            if (len(randomChip.Cores[CoreId].TasksList) > 0):
                tList = randomChip.Cores[CoreId].TasksList

        task = random.choice(tList)

        # find second random core
        rChip = random.choice(c)
        rChoice = list(rChip.Cores.keys())
        rCoreId = random.choice(rChoice)
        rtList = []

        # half the time move random task, half the time swap 2 random tasks
        prob = random.uniform(0,1)
        if (0.5 > prob ):
            # remove task from old core
            randomChip.Cores[CoreId].removeTask(task)
            # add task to new core
            rChip.Cores[rCoreId].addTask(task)

        else:
            # have to find a non-empty second core to be able to swap
            while len(rtList) == 0:
                rChip = random.choice(c)
                rChoice = list(rChip.Cores.keys())
                rCoreId = random.choice(rChoice)
                if (len(rChip.Cores[rCoreId].TasksList) > 0):
                    rtList = rChip.Cores[rCoreId].TasksList

            rTask = random.choice(rtList)

            tmp = copy.deepcopy(rTask)
            rTask = task
            task = tmp

    # Sort the neighbour at the end
    for chip in c:
        for coreId in chip.Cores:
            curr_core = chip.Cores[coreId]
            curr_core.sortList()

    return c


# Something
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

            # iterating over list

            for t in curr_core.TasksList:
                if int(t.Deadline) < prevTaskDeadline and prevTaskDeadline != 0:
                    cost += 1 + numUnordered * orderWeight
                    numUnordered += 1

                elif int(t.Deadline) == prevTaskDeadline:
                    if int(t.WCET) > prevTaskWCET:
                        cost += 1 + numUnordered * orderWeight
                        numUnordered += 1

                prevTaskDeadline = int(t.Deadline)
                prevTaskWCET = int(t.WCET)

                taskCount += 1
                cost += taskCount * taskCountWeight
                cost += float(curr_core.WCETFactor) * float(t.WCET)


    # If neighbour is not a solution, add massive penalty
    feasible = isSolution(chips)
    if (not feasible):
        cost += nonFeasibleWeight

    return cost

# Checks if solution is scheduble 
def isSolution(solution, lax=[]):
    tl = 0
    feasible = True
    for chip in solution:
        for coreID in chip.Cores:
            # WCETFactor & Tasks
            i = 0.0
            curr_core = chip.Cores[coreID]

            for t in curr_core.TasksList:
                responseTime = i + float(curr_core.WCETFactor) * float(t.WCET) # How long the task takes in this specific core
                i = responseTime
                tl += i

                if responseTime > float(t.Deadline):
                    feasible = False

    lax.append(tl)
    return feasible

