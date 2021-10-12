import xml.etree.ElementTree as ET
from operator import attrgetter
import random
from simulatedAnnealing import *

tasks = []
chips = []
c_t = {}
tree = ET.parse('../large.xml')
root = tree.getroot()


# Reading from xml

class Task:

    def __init__(self, Id, Period, Deadline, WCET):
        self.Id = Id
        self.Period = Period
        self.Deadline = Deadline
        self.WCET = WCET

    def __str__(self):
        return "    Id: " + self.Id + ", Period: " + self.Period + ", Deadline: " + self.Deadline + ", WCET: " + self.WCET

    def __eq__(self, other):
        if isinstance(other, Task):
            return self.Id == other.Id

class Core:

    def __init__(self, Id, WCETFactor):
        self.Id = Id
        self.WCETFactor = WCETFactor
        self.Tasks = {}
        self.TasksList = []

    #337413.7
    #286176.2

    def addTask(self, Task):
        self.Tasks[Task.Id] = Task
        self.TasksList.append(Task)

    def removeTask(self, Task):
        del self.Tasks[Task.Id]
        self.TasksList.remove(Task)

    def __str__(self):
        string = " coreId : " + self.Id + ", WCETFactor: " + self.WCETFactor

        for Id in self.Tasks:
            print(self.Tasks[Id])

        return string

    def __eq__(self, other):
        if isinstance(other, Core):
            return self.Id == other.Id and self.WCETFactor == other.WCETFactor and self.Tasks == other.Tasks
        return False
    
    def sortList(self):
        self.TasksList.sort(key=lambda x: (x.Deadline, -int(x.WCET)))    # source : https://www.techiedelight.com/sort-list-of-objects-by-multiple-attributes-python/


class Chip:

    def __init__(self, Id):
        self.Id = Id
        self.Cores = {}

    def addCore(self, Core):
        self.Cores[Core.Id] = Core

    def __str__(self):
        string = "Chip ID: " + self.Id

        for Id in self.Cores:
            print(self.Cores[Id])

        return string

    def __eq__(self, other):
        if isinstance(other, Chip):
            return self.Id == other.Id and self.Cores == other.Cores
        return False



for child in root:
    if child.tag == "Application":
        for g_child in child:
            newTask = Task(Id=g_child.attrib['Id'], Period=g_child.attrib['Period'], Deadline=g_child.attrib['Deadline'], WCET=g_child.attrib['WCET'])
            tasks.append(newTask)

    if child.tag == "Platform":
        for g_child in child:
            #Ini Chips
            newChip = Chip(g_child.attrib['Id'])
            for g_g_child in g_child:
                #Ini Cores
                newCore = Core(Id=g_g_child.attrib['Id'], WCETFactor=g_g_child.attrib['WCETFactor'])
                newChip.addCore(newCore)    #TODO remove newCore.Id from the value field
            chips.append(newChip)

# Randomize initial solution
for item in tasks:
    randomChip = random.choice(chips)

    choice = list(randomChip.Cores.keys())

    CoreId = random.choice(choice)

    randomChip.Cores[CoreId].addTask(item)

# Sort tasks in initial solution
# for chip in chips:
#     for coreID in chip.Cores:
#         curr_core = chip.Cores[coreID]
#         curr_core.sortList()
            
print('randomizedSolution is a solution: ', str(isSolution(chips)))

# 178610.1 - 1
# 178595.1 - 2
# 178595.9 - 3

# get cost before, run SA, get cost after and print solution
c = Cost(chips)
new = simulatedAnnealing(chips)
print("")
for chip in new:
    print(chip)
print("")
print("Is init a solution: " + str(isSolution(chips)))
print("Is result a solution: " + str(isSolution(new)))
print("")
print(c)
print("-------------------------------")
print(Cost(new))
