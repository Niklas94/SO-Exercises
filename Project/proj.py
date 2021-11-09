from parsexml import *
import copy

# vertices, edges, msgs = parse("Config.xml", "Apps.xml")
vertices, edges, msgs = parse()

def stuck(curr,visited):
    ret = True
    for e in vertices[curr].Egress:
        if e.Destination not in visited:
            ret = False
    return ret


# Generates an array of arrays. Each inner array is a route for a message.
def initSolution():
    sol = []
    for m in msgs:
        curr = m.Source
        visited = []
        stack = []
        msg2r = Msg2Route(m)

        while (curr != m.Destination):
            # check if the edges going out of current vertex are already
            # assigned to queues. If not, pick random queues from 1 to the total
            # number of outgoing edges to assign each edge.            
            if (len(vertices[curr].Egress) > 0):
                unset = vertices[curr].Egress[0].Queue == 0
                if unset:
                    e_len = len(vertices[curr].Egress)
                    for i in range (0, e_len):
                        rand = random.randint(1,e_len)
                        vertices[curr].Egress[i].Queue = rand

            # Check if the search destination is the destination of one of the
            # outgoing edges
            for edge in vertices[curr].Egress:
                if edge.Destination == m.Destination:
                    curr = edge.Destination
                    e = edge
                    break

            # If we're not at the goal, get next vertex
            if curr != m.Destination:
                visited.append(curr)
                stack.append(curr)
                # If stuck go back to the node you just came from and try
                # another way
                while stuck(curr,visited):
                    msg2r.Route.pop(len(msg2r.Route)-1)
                    stack.pop(len(stack)-1)
                    curr = stack[len(stack)-1]

                e_len = len(vertices[curr].Egress)
                ran_num = random.randint(1,e_len)
                # If the randomly picked outgoing edge is already visited, pick
                # another random number
                while (vertices[curr].Egress[ran_num-1].Destination in visited):
                    ran_num = random.randint(1,e_len)
                e = vertices[curr].Egress[ran_num-1]
                curr = vertices[curr].Egress[ran_num-1].Destination

            msg2r.Route.append(e)
        sol.append(msg2r)
    return sol

for r in initSolution():
    print(r)
    print()
