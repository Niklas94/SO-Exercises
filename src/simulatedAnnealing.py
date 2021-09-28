import random
import math
import copy

# Algorithm 5 - Exercises week 37
def simulatedAnnealing(initialSolution):
    T = 10000000000000  # Temperature - Fixed value
    r = 0.999    # Pick value between 0.8 - 0.99
    C = initialSolution
    curr_best = copy.deepcopy(initialSolution)
    l = [] # set/array of solutions

    while (T > 1):
        CP = neighbourhood(C)
        prob = random.uniform(0,1)
        if (AccProbability(Cost(C), Cost(CP), T) > prob):
            C = CP
            if (isSolution(C)):
                if (Cost(C) < Cost(curr_best)):
                    curr_best = copy.deepcopy(C)
                # l.append(C)
        T = T * r

    return curr_best

# Find 'nearby' solution
def neighbourhood (chips):
    c = copy.deepcopy(chips)

    tChoice = []
    while len(tChoice) == 0:
        randomChip = random.choice(c)
        choice = list(randomChip.Cores.keys())
        CoreId = random.choice(choice)

        # get a random task out, if none return current solution
        tChoice = list(randomChip.Cores[CoreId].Tasks.keys())

    task = randomChip.Cores[CoreId].Tasks[random.choice(tChoice)]

    # find second random core
    rChip = random.choice(c)
    rChoice = list(rChip.Cores.keys())
    rCoreId = random.choice(rChoice)

    # remove task from old core
    randomChip.Cores[CoreId].removeTask(task)
    # add task to new core
    rChip.Cores[rCoreId].addTask(task)

    return c


# Something
def AccProbability(costCurrent, costNeighbour, T):
    if (costCurrent > costNeighbour):
        return 1.1
    else:
        return math.exp( (costCurrent - costNeighbour) / T)

# Penalty function
def Cost(chips):
    cost = 0

    for chip in chips:
        for coreID in chip.Cores:
            taskCount = 0
            prevTaskDeadline = 0
            numUnordered = 0
            for taskId in chip.Cores[coreID].Tasks:
                curr_task = chip.Cores[coreID].Tasks[taskId]
                if int(curr_task.Deadline) < prevTaskDeadline and prevTaskDeadline != 0:
                    cost += 1 + numUnordered
                    numUnordered += 1
                prevTaskDeadline = int(curr_task.Deadline)

                taskCount += 1
                cost += taskCount

    return cost

# Checks if solution is scheduble 
def isSolution(solution):
    for chip in solution:
        for coreID in chip.Cores:
            # WCETFactor & Tasks
            acc = 0.0
            curr_core = chip.Cores[coreID]

            for taskId in curr_core.Tasks:
                curr_task = chip.Cores[coreID].Tasks[taskId]
                acc += float(curr_task.WCET) * float(curr_core.WCETFactor)

                if acc > float(curr_task.Deadline):
                    return False

    return True
