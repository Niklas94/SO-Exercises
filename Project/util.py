from simulatedAnnealing import *

# Generates an array of arrays. Each inner array is a route for a message.
def initSolution(msgs,vertices):
    solution : Solution = Solution()
    routes : List[Route] = []

    for m in msgs:
        curr : str = m.Source
        route : Route = Route(m)

        # Do a search from current to m.destination. Route will be appended to
        # the route object by reference.
        search(curr,[],[],route,vertices)
        routes.append(route)

    solution.Routes = routes

    return solution

# Take arr with 9 floats. [0] is totalDone, [1] firstFeasibleTime, [2] bestDone,
# [3] tried, [4] bestCount, [5] costBefore, [6] costAfter, [7] costImprove, [8]
# feasibles. Sums into these 9 floats by reading the data from file.
def SumLines(arr : List[float]):
    f = open("file.txt", "r")
    # Sum the different values. Averaging is done in the strings afterwards.
    lines = f.readlines()
    for line in lines:
        curr = line.split()
        # totalDone
        arr[0] += float(curr[0])
        # firstFeasibleTime
        if (float(curr[1]) > 0.0):
            arr[1] += float(curr[1])
        # bestDone
        arr[2] += float(curr[2])
        # tried
        arr[3] += int(curr[3])
        # bestCount
        arr[4] += int(curr[4])
        # costBefore
        arr[5] += float(curr[5])
        # costAfter
        arr[6] += float(curr[6])
        # costImprove
        if (float(curr[7]) > 0.0):
            arr[7] += float(curr[7])
        # feasibles
        if curr[9] == "True":
            arr[8] += 1

# Print statistics to standard out and write them to out.txt as well.
def PrintAndWrite(arr, fileDescriptor, file, iterations):
    totalDone = arr[0]
    firstFeasibleTime = arr[1]
    bestDone = arr[2]
    tried = arr[3]
    bestCount = arr[4]
    costBefore = arr[5]
    costAfter = arr[6]
    costImprove = arr[7]
    feasibles = arr[8]

    m1 = "Statistics for {path:s} run {it:d} times.".format(path = file, it
                                                            = iterations)
    m2 = "Average time to done was {time:.2f}s".format(time = totalDone /
                                                       iterations)
    if feasibles > 0.0:
        m3 = "Average time to first feasible solution was {time:.2f}s".format(time =
                                                                              firstFeasibleTime
                                                                              /
                                                                              feasibles)
        m4 = "Average time to find the last found best solution was {time:.2f}s".format(time = bestDone / feasibles)
        m6 = "Average times a new best solution was found was {be:.2f}".format(be
                                                                             =
                                                                             bestCount
                                                                             /
                                                                             feasibles)
        m9 = "Average cost improvement from first feasible to last was {co:.2f}".format(co = costImprove / feasibles)
    else:
        m3 = "No feasible solution, so no avg. time for first"
        m4 = "No feasible solution, so no avg. time for last best found"
        m6 = "No feasible solution, so no avg. times a new best was found"
        m9 = "No feasible solution, so no avg. cost improvement"
    m5 = "Average solutions tried was {tri:.2f}".format(tri = tried /
                                                      iterations)
    m7 = "Average cost before running simulated annealing was {co:.2f}".format(co = costBefore / iterations)
    m8 = "Average cost after running simulated annealing was {co:.2f}".format(co = costAfter / iterations)
    m10 = "{feas:d} out of {tot:d} ended in feasible solutions.".format(feas =
                                                                       int(feasibles),
                                                                       tot =
                                                                       iterations)
    strings = [m1, m2, m3, m4, m5, m6, m7, m8, m9, m10]
    for s in strings:
        print(s)
    print()
    fileDescriptor.write(m1 + "\n" + m2+ "\n" + m3 + "\n"+ m4 + "\n"+ m5 + "\n"
                         + m6 + "\n"+ m7 + "\n"+ m8 + "\n"+ m9 + "\n" + m10 +
                         "\n")

# Runs simulated annealing "iterations" times for each path in "filePaths",
# outputting statistics about (1) average run time, (2) average time before the
# best solution was found, (3) average number of tried solutions, (4) average
# number of times a new best was found, (5) average cost before simulated
# annealing, (6) average cost after, (7) average cost improvement and (8) how
# many feasible solutions were found in total.
def runStatistics(iterations : int, filePaths : List[str]):
    l = open("out.txt", "w")
    for file in filePaths:
        vertices, edges, msgs = parse(file + "Config.xml", file + "Apps.xml")
        f = open("file.txt", "w")
        f.close()

        for _ in range(0,iterations):
            s = initSolution(msgs,vertices)

            simulatedAnnealing(s, vertices, edges, True)

        arr = [0.0] * 9
        SumLines(arr)
        PrintAndWrite(arr, l, file, iterations)

    print("Output written to out.txt")
    l.close()

# Runs simulated annealing once on given files and returns solution
def runOnce(filePath : str):
    vertices, edges, msgs = parse(filePath + "Config.xml", filePath + "Apps.xml")
    s = initSolution(msgs, vertices)
    c = simulatedAnnealing(s, vertices, edges, False)

    return c

