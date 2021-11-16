from parsexml import *
from simulatedAnnealing import *
from vsearch import *
import copy

# vertices, edges, msgs = parse("Config.xml", "Apps.xml")
vertices, edges, msgs = parse()

# Generates an array of arrays. Each inner array is a route for a message.
def initSolution() -> list[Route]:
    sol : list[Route] = []
    for m in msgs:
        curr : str = m.Source
        route : Route = Route(m)

        # Do a search from current to m.destination. Route will be appended to
        # the route object by reference.
        search(curr,[],[],route,vertices)
        sol.append(route)
    return sol

s : list[Route] = initSolution()
for r in s:
    print(r)
    print()

# neighbourhood(s,vertices)

# print("After neighbourhood")
# print("-------------------")
# for r in s:
#     print(r)
#     print()
