from parsexml import *
from simulatedAnnealing import *
from vsearch import *
import copy

# vertices, edges, msgs = parse("Config.xml", "Apps.xml")
vertices, edges, msgs = parse()

# Generates an array of arrays. Each inner array is a route for a message.
def initSolution():
    sol = []
    for m in msgs:
        curr = m.Source
        msg2r = Msg2Route(m)

        # Do a search from current to m.destination. Route will be appended to
        # the msg2r object by reference.
        search(curr,[],[],msg2r,vertices)
        sol.append(msg2r)
    return sol

s = initSolution()
#for r in s:
#    print(r)
#    print()

neighbourhood(s,vertices)

print("After neighbourhood")
print("-------------------")
for r in s:
    print(r)
    print()

linkConstraint = linkCapacityConstraint(s)

print("linkConstraintUpheld: " + str(linkConstraint))