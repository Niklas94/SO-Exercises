from parsexml import *
import copy

vertices, edges, msgs = parse()

def initSolution():
    msg = msgs[0]
    visited = []

    curr = msg.Source
    d = []
    while (len(d) == 0):
        # Check if the search destination is the destination of one of the outgoing
        # edges
        for e in vertices[curr].Egress:
            if e.Destination == msg.Destination:
                ind = (vertices[curr].Egress).index(e)
                curr = vertices[curr].Egress[ind].Destination

        l = len(vertices[curr].Egress)
        c = random.randint(0,l)
        if curr == msg.Destination:
            d.append(curr)
        else:
            visited.append(curr)
            # If the randomly picked outgoing edge is already visited, pick another
            # random number
            while (vertices[curr].Egress[c-1] in visited):
                c = random.randint(0,l)
            curr = vertices[curr].Egress[c-1].Destination
        print(curr)
    return d

print(initSolution())
