from parsexml import *

def stuck(curr, visited, vertices):
    ret = True
    for e in vertices[curr].Egress:
        if e.Destination not in visited:
            ret = False
    return ret

def search(cur, vis, sta, route, vertices):
    curr : str = cur
    visited : list[str] = vis
    stack : list[str] = sta
    destination : str = route.Msg.Destination
    while (curr != destination):
        # check if the edges going out of current vertex are already
        # assigned to queues. If not, pick random queues from 1 to the total
        # number of outgoing edges to assign each edge.            
        # if (len(vertices[curr].Egress) > 0):
        #     unset = vertices[curr].Egress[0].Queue == 0
        #     if unset:
        #         e_len = len(vertices[curr].Egress)
        #         for i in range (0, e_len):
        #             rand = random.randint(1,e_len+1)
        #             vertices[curr].Egress[i].Queue = rand

        # Check if the search destination is the destination of one of the
        # outgoing edges
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

        route.LinkAssignments.append(LinkAssignment(e, random.randint(1, 3)))
        # Always multiplies by queue even if it might be send earlier due to T %
        # q == 0
    return route