from parsexml import *
import random
from typing import List

# Returns false if not stuck (if has somewhere to go that has not already been
# visited) at current position. Returns true if nowhere to go that hasn't
# already been visited.
def stuck(curr, visited, vertices):
    ret = True
    for e in vertices[curr].Egress:
        if e.Destination not in visited:
            ret = False
    return ret

# Search for a route between cur and route.Msg.Destination, append link
# assignments taken to the route and return it.
def search(cur, vis, sta, route, vertices):
    curr : str = cur
    visited : List[str] = vis
    stack : List[str] = sta
    destination : str = route.Msg.Destination
    while (curr != destination):
        # Check if the search destination is the destination of one of the
        # outgoing edges, if so, create link assignment from the edge leading
        # there, add to the route, and return the route.
        for edge in vertices[curr].Egress:
            if edge.Destination == destination:
                curr = edge.Destination
                e = edge
                break

        # If we're not at the goal, get next vertex
        if curr != destination:
            visited.append(curr)
            stack.append(curr)
            # If stuck go back to the node you just came from and try
            # another way
            while stuck(curr,visited,vertices):
                route.LinkAssignments.pop(len(route.LinkAssignments)-1)
                stack.pop(len(stack)-1)
                curr = stack[len(stack)-1]

            e_len : int = len(vertices[curr].Egress)
            ran_num : int = random.randint(1,e_len)
            # If the randomly picked outgoing edge is already visited, pick
            # another random number
            while (vertices[curr].Egress[ran_num-1].Destination in visited):
                ran_num = random.randint(1,e_len)
            e : Edge = vertices[curr].Egress[ran_num-1]
            curr = vertices[curr].Egress[ran_num-1].Destination

        randomQueue = random.randint(1,3)
        route.LinkAssignments.append(LinkAssignment(e, randomQueue))
        route.Id += str(e.Id) + str(randomQueue)
    return route
