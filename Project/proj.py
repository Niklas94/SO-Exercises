from parsexml import *
from simulatedAnnealing import *
from vsearch import *
import time
from typing import List
from solutionToXml import solutionToXml

start_time = time.time()
# vertices, edges, msgs = parse("ConfigTest.xml", "AppsTest.xml")
vertices, edges, msgs = parse("test cases/Small/TC1/Input/Config.xml", "test cases/Small/TC1/Input/Apps.xml")
# vertices, edges, msgs = parse("test cases/Medium/TC4/Input/Config.xml", "test cases/Medium/TC4/Input/Apps.xml")
# vertices, edges, msgs = parse("test cases/Small/TC1/Input/Config.xml", "test cases/Small/TC1/Input/Apps.xml")
# vertices, edges, msgs = parse()

# Generates an array of arrays. Each inner array is a route for a message.
def initSolution():
    sol : List[Route] = []

    for m in msgs:
        curr : str = m.Source
        route : Route = Route(m)

        # Do a search from current to m.destination. Route will be appended to
        # the route object by reference.
        search(curr,[],[],route,vertices)
        sol.append(route)
    return sol

s = initSolution()

c = simulatedAnnealing(s, vertices, edges)

runtime = time.time() - start_time


# Needs the variables ObjectiveValue and MeanE2E
solutionToXml(runtime, 100, 200, s)

