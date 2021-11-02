# SO-Exercises
System Optimization Exercises

### Version >=3.8 of Python used when writing and testing.

## Description
The Simulated Annealing code is located in the **simulatedAnnealing.py** file,
while the code that parses the XML input files and generates a solution is
**parsexml.py**. Here a random initial solution is generated, simulated
annealing is run on it. If a solution is found, the result is written into the
**solution.xml** file. If no solution could be found, a print to the terminal
will inform of this.

## How to run
The input file has to be put up one level from the  **parsexml.py** file. The
input file to be run on can be changed in the **parsexml.py** file at the top.
To run the code simply run parsexml.py with python by issuing the command
``python parsexml.py''.
