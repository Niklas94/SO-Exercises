from parsexml import *
import copy

vertices, edges, msgs = parse()

def stuck(curr,visited):
    ret = True
    for e in vertices[curr].Egress:
        if e.Destination not in visited:
            ret = False
    return ret


def initSolution():
    msg = msgs[0]
    curr = msg.Source
    visited = []
    route = [vertices[curr].Name]
    stack = []

    while (curr != msg.Destination):
        # Check if the search destination is the destination of one of the outgoing
        # edges
        for edge in vertices[curr].Egress:
            if edge.Destination == msg.Destination:
                curr = edge.Destination
                break

        if curr != msg.Destination:
            visited.append(curr)
            stack.append(curr)
            # If stuck go back to the node you just came from and try another
            # way
            while stuck(curr,visited):
                route.pop(len(route)-1)
                stack.pop(len(stack)-1)
                curr = stack[len(stack)-1]
            e_len = len(vertices[curr].Egress)
            ran_num = random.randint(1,e_len)
            # If the randomly picked outgoing edge is already visited, pick another
            # random number
            while (vertices[curr].Egress[ran_num-1].Destination in visited):
                ran_num = random.randint(1,e_len)
            curr = vertices[curr].Egress[ran_num-1].Destination

        route.append(curr)
    return route

print(initSolution())
