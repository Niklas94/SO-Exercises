import random
import math
import copy


# Algorithm 5 - Exercises week 37
def simulatedAnnealing(initialSolution):
    T = 100000000000  # Temperature - Fixed value
    r = 0.999    # Pick value between 0.8 - 0.99
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
        #print(prob)
        if (0.5 > prob ):
            # remove task from old core
            randomChip.Cores[CoreId].removeTask(task)
            # add task to new core
            rChip.Cores[rCoreId].addTask(task)            
            
        # elif 0.33 < prob and prob < 0.66:
        #     # sort a cores tasks
        #     rChip.Cores[rCoreId].sortList()
            
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

    # Sort the neighbour at the end
    for chip in c:
        for coreId in chip.Cores:
            curr_core = chip.Cores[coreId]
            curr_core.sortList()
	    #for coreID in chip.Cores:
        #    print(coreID)
            #curr_core = chip.Cores[coreID]
            #curr_core.sortList()

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
            
            for e in curr_core.TasksList:
                if int(e.Deadline) < prevTaskDeadline and prevTaskDeadline != 0:
                     cost += 1 + numUnordered * orderWeight
                     numUnordered += 1

                elif int(e.Deadline) == prevTaskDeadline:
                    if int(e.WCET) > prevTaskWCET:
                        cost += 1 + numUnordered * orderWeight
                        numUnordered += 1

                prevTaskDeadline = int(e.Deadline)
                prevTaskWCET = int(e.WCET)

                taskCount += 1
                cost += taskCount * taskCountWeight
                cost += float(curr_core.WCETFactor) * float(e.WCET)
                
            # # iterating over dict
            # for taskId in curr_core.Tasks:
            #     curr_task = curr_core.Tasks[taskId]
            #     # If tasks are not ordered according to deadline, then penalize (we want lowest deadline first)
            #     if int(curr_task.Deadline) < prevTaskDeadline and prevTaskDeadline != 0:
            #          cost += 1 + numUnordered * orderWeight
            #          numUnordered += 1
            #     # If tasks have same deadline, but unordered according to WCET, then penalize as well (we want highest WCET first)
            #     elif int(curr_task.Deadline) == prevTaskDeadline:
            #         if int(curr_task.WCET) > prevTaskWCET:
            #             cost += 1 + numUnordered * orderWeight
            #             numUnordered += 1

            #     prevTaskDeadline = int(curr_task.Deadline)
            #     prevTaskWCET = int(curr_task.WCET)

            #     taskCount += 1
            #     # Penalize depending on amount of tasks in core (1, 3, 6, 10, 15, 21...)
            #     cost += taskCount * taskCountWeight
            #     # hopefully this means that tasks with horrible WCET will get
            #     # tasked to fast cores
            #     cost += float(curr_core.WCETFactor) * float(curr_task.WCET)
            #print('cost for core:', coreID, cost)
            #print('cost before WCET : ', cost)
            
                #print('cost of unordered, WCET and taskCount: ', 1 + numUnordered * orderWeight, float(curr_core.WCETFactor) * float(curr_task.WCET), taskCount * taskCountWeight)



    # If neighbour is not a solution, add massive penalty
    feasible = isSolution(chips)
    if (not feasible):
        cost += nonFeasibleWeight

    #print('total cost: ')
    #print(cost)

    return cost

# Checks if solution is scheduble 
def isSolution(solution):
    feasible = True
    for chip in solution:
        for coreID in chip.Cores:
            # WCETFactor & Tasks
            i = 0.0
            curr_core = chip.Cores[coreID]

            for e in curr_core.TasksList:
                # curr_task = chip.Cores[coreID].Tasks[taskId]

                responseTime = i + float(curr_core.WCETFactor) * float(e.WCET) # How long the task takes in this specific core
                i = responseTime

                # print(str(responseTime) + " > " + curr_task.Deadline)
                if responseTime > float(e.Deadline):
                    feasible = False

    return feasible
