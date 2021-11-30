import time
from util import *
from solutionToXml import solutionToXml


# Run several full simulated annealing iterations of multiple files
# testPaths = []
# testPaths.append("test cases/Small/TC1/Input/")
# testPaths.append("test cases/Medium/TC4/Input/")
# testPaths.append("test cases/Large/TC7/Input/")
# runStatistics(10, testPaths)

# Run single simulated annealing iteration on single file, output solution to
# Report.xml
start_time = time.time()
c = runOnce("test cases/Small/TC1/Input/")
runtime = time.time() - start_time
c.CalculateMeanE2E()
solutionToXml(runtime, c)
