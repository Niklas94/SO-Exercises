import random
import math


# Algorithm 5 - Exercises week 37
def simulatedAnnealing(initialSolution: dict):
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
def neighbourhood (tasks, cores):
     randomTask = random.choice(tasks)
     randomCore= random.choice(cores)
     randomTask['MCP'] = randomCore['mcpID']
     randomTask['Core'] = randomCore['Id']

# Something
def AccProbability(costCurrent, costNeighbour, T):
    if (costCurrent > costNeighbour):
        return 1.1
    else
        return math.exp( (costCurrent - costNeighbour) / T) 
    
# Penalty function
def Cost(solution: dict):

    cost = 0
    
    for (chipId, coreId), taskId in solution.items():
        # key = (0, 2)
        # value = [0, 2]
        I = 0
        for item in value:
            


    return 1

# Checks if solution is scheduble 
def isSolution(solution: dict):
    
    for (chipId, coreId), taskId in solution.items():
        # Value : 
    
    return true