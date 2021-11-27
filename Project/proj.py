from parsexml import *
from simulatedAnnealing import *
from vsearch import *

# vertices, edges, msgs = parse("ConfigTest.xml", "AppsTest.xml")
# vertices, edges, msgs = parse("test cases/Large/TC7/Input/Config.xml", "test cases/Large/TC7/Input/Apps.xml")
vertices, edges, msgs = parse("test cases/Medium/TC4/Input/Config.xml", "test cases/Medium/TC4/Input/Apps.xml")
# vertices, edges, msgs = parse("test cases/Small/TC1/Input/Config.xml", "test cases/Small/TC1/Input/Apps.xml")
# vertices, edges, msgs = parse()

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
sc = Cost(s)

c = simulatedAnnealing(s, vertices, edges)
cc = Cost(c)

print("Cost before: " + str(sc) + ", cost after: " + str(cc))
