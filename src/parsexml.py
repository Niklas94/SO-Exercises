import xml.etree.ElementTree as ET
from operator import attrgetter
import random
from simulatedAnnealing import *
from xml.dom import minidom

tasks = []
chips = []
tree = ET.parse('../large.xml')
root = tree.getroot()

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
        self.TasksList = []

    def addTask(self, Task):
        self.TasksList.append(Task)

    def removeTask(self, Task):
        self.TasksList.remove(Task)

    def __str__(self):
        string = " coreId : " + self.Id + ", WCETFactor: " + self.WCETFactor
        for task in self.TasksList:
            print(task)
        return string

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

# Run simulated annealing on the initial solution
new = simulatedAnnealing(chips)
# Lax is used to get the total laxity. We use it in the isSolution function
# where we pass it by reference.
lax = []

if (isSolution(new, lax)):
    print("Solution found. Check solution.xml for result.")
    data = ET.Element('solution')

    for chip in new:
        for coreID in chip.Cores:
            curr_core = chip.Cores[coreID]  # Get current core
            i = 0.0
            for t in curr_core.TasksList:   # Get all tasks for that core
                responseTime = i + float(curr_core.WCETFactor) * float(t.WCET) # How long the task takes in this specific core
                i = responseTime
                task = ET.SubElement(data, 'Tasks')
                task.set('id', t.Id)
                task.set('MCP', chip.Id)
                task.set('Core', coreID)
                task.set('WCRT', str(int(responseTime)))

    xmlstr = minidom.parseString(ET.tostring(data, encoding='unicode', method='xml')).toprettyxml(indent="   ")

    outfile = open("solution.xml", "w")
    outfile.write(xmlstr)
    outfile.write("<!-- Total Laxity: " + str(int(lax[0])) + " -->")
else:
    print("Solution could not be found.")
