import random
import math

# Algorithm 5 - Exercises week 37
def simulatedAnnealing(initialSolution):
    T = 10000   # Temperature - Fixed value
    r = 0.99    # Pick value between 0.8 - 0.99
    C = initialSolution
    l = [] # set/array of solutions

    while (T > 1):
        CP = neighbourhood(C)
        if (AccProbability(Cost(C), Cost(CP), T) > random.uniform(0, 1)):
            C = CP
            if (isSolution(C)):
                l.append(C)
        T = T * r

    return l

# Find 'nearby' solution
def neighbourhood (chips):
    # find first random core
    randomChip = random.choice(chips)
    choice = list(randomChip.Cores.keys())
    CoreId = random.choice(choice)

    # get a random task out, if none return current solution
    tChoice = list(randomChip.Cores[CoreId].Tasks.keys())
    if len(tChoice) == 0:
        return chips

    task = randomChip.Cores[CoreId].Tasks[random.choice(tChoice)]

    # find second random core
    rChip = random.choice(chips)
    rChoice = list(rChip.Cores.keys())
    rCoreId = random.choice(rChoice)

    # remove task from old core
    randomChip.Cores[CoreId].removeTask(task)
    # add task to new core
    rChip.Cores[rCoreId].addTask(task)

    return chips


# Something
def AccProbability(costCurrent, costNeighbour, T):
    print("Curr: " + str(costCurrent) + ", neigh: " + str(costNeighbour) + ", T: " + str(T))
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
