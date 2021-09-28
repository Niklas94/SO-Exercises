import random
import math
import copy

# Algorithm 5 - Exercises week 37
def simulatedAnnealing(initialSolution):
    T = 10000000000000  # Temperature - Fixed value
    r = 0.999    # Pick value between 0.8 - 0.99
    C = initialSolution
    curr_best = copy.deepcopy(initialSolution)

    while (T > 1):
        print(T)
        CP = neighbourhood(C)
        prob = random.uniform(0,1)
        if (AccProbability(Cost(C), Cost(CP), T) > prob):
            # print("Curr best: " + str(Cost(curr_best)))
            # print("Picking " + str(Cost(CP)) + " over " + str(Cost(C)))
            C = CP
            if (isSolution(C)):
                curr_best = copy.deepcopy(C)
        T = T * r

    return curr_best

# Find 'nearby' solution
def neighbourhood (chips):
    c = copy.deepcopy(chips)

    for i in range (0,5):
        # find first random core
        tChoice = []
        while len(tChoice) == 0:
            randomChip = random.choice(c)
            choice = list(randomChip.Cores.keys())
            CoreId = random.choice(choice)
            tChoice = list(randomChip.Cores[CoreId].Tasks.keys())

        task = randomChip.Cores[CoreId].Tasks[random.choice(tChoice)]

        # find second random core
        rChip = random.choice(c)
        rChoice = list(rChip.Cores.keys())
        rCoreId = random.choice(rChoice)
        rtChoice = []

        # half the time move random task, half the time swap 2 random tasks
        prob = random.uniform(0,1)
        if (0.5 > prob):
            # remove task from old core
            randomChip.Cores[CoreId].removeTask(task)
            # add task to new core
            rChip.Cores[rCoreId].addTask(task)

        else:
            # have to find a non-empty second core to be able to swap
            while len(rtChoice) == 0:
                rChip = random.choice(c)
                rChoice = list(rChip.Cores.keys())
                rCoreId = random.choice(rChoice)
                rtChoice = list(rChip.Cores[rCoreId].Tasks.keys())

            rTask = rChip.Cores[rCoreId].Tasks[random.choice(rtChoice)]

            tmp = copy.deepcopy(rTask)
            rTask = task
            task = tmp

    # sort tasks by deadline in cores before returning solution
    for chip in c:
        for coreID in chip.Cores:
            tD = copy.deepcopy(chip.Cores[coreID].Tasks)
            chip.Cores[coreID].Tasks = dict(sorted(tD.items(), key = lambda x :
                                                   int(x[1].Deadline)))

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
            curr_core = chip.Cores[coreID]
            # prevTaskDeadline = 0
            # numUnordered = 0
            for taskId in curr_core.Tasks:
                curr_task = curr_core.Tasks[taskId]
                # if int(curr_task.Deadline) < prevTaskDeadline and prevTaskDeadline != 0:
                #     cost += 1 + numUnordered
                #     numUnordered += 1
                # prevTaskDeadline = int(curr_task.Deadline)

                taskCount += 1
                # hopefully this means that tasks with horrible WCET will get
                # tasked to fast cores
                cost += taskCount * (float(curr_core.WCETFactor) *
                                     float(curr_task.WCET))

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
