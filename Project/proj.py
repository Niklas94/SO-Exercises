from parsexml import *
from simulatedAnnealing import *
from vsearch import *
# import copy

# vertices, edges, msgs = parse("Config.xml", "Apps.xml")
vertices, edges, msgs = parse("test cases/Medium/TC4/Input/Config.xml", "test cases/Medium/TC4/Input/Apps.xml")

# Generates an array of arrays. Each inner array is a route for a message.
def initSolution():
    sol : list[Route] = []

    for m in msgs:
        curr : str = m.Source
        route : Route = Route(m)

        # Do a search from current to m.destination. Route will be appended to
        # the route object by reference.
        search(curr,[],[],route,vertices)
        sol.append(route)
    return sol

s = initSolution()
# for r in s:
#     print(r)
#     print()
sc = Cost(s, calculateHyperCycleLength(s), edges)

c = simulatedAnnealing(s, vertices, edges)
# neighbourhood(s,vertices)
cc = Cost(c, calculateHyperCycleLength(c), edges)

print("Cost before: " + str(sc) + ", cost after: " + str(cc))
# if c != None:
#     print("After neighbourhood")
#     print("-------------------")
#     for r in c:
#         print(r)
#         print()
