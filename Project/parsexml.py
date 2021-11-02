import xml.etree.ElementTree as ET
from operator import attrgetter
import random
from simulatedAnnealing import *
from xml.dom import minidom

vertices = {}
edges = []
conf_tree = ET.parse('Config.xml')
conf_root = conf_tree.getroot()
app_tree = ET.parse('Apps.xml')
app_root = app_tree.getroot()

class Vertex:
    def __init__(self, Name):
        self.Name = Name
        self.Ingress = []
        self.Egress = []

    def __str__(self):
        ret =  "Name: " + self.Name + "\nIngress: "
        for i in self.Ingress:
            ret += "\n" + i.__str__() + ", "
        ret += "\nEgress: "
        for e in self.Egress:
            ret + "\n" + e.__str__() + ", "
        return ret + "\n"


class Edge:
    def __init__(self, Id, Bandwidth, PropDelay, Source, Destination):
        self.Id = Id
        self.Bandwidth = Bandwidth
        self.PropDelay = PropDelay
        self.Source = Source
        self.Destination = Destination

    def __str__(self):
        return ("    Id: " + self.Id + ", Bandwidth: " + self.Bandwidth + ", PropDelay: " + self.PropDelay + ", Source: " + self.Source + ", Destination: " + self.Destination)

    def __eq__(self, other):
        if isinstance(other, Edge):
            return self.Id == other.Id

class Message:
    def __init__(self, Name, Source, Destination, Size, Period, Deadline):
        self.Name = Name
        self.Source = Source
        self.Destination = Destination
        self.Size = Size
        self.Period = Period
        self.Deadline = Deadline

    def __str__(self):
        return ("    Name: " + self.Name + ", Source: " + self.Source + ", Destination: " + self.Destination + ", Size: " + self.Size + ", Period: " + self.Period + ", Deadline: " + self.Deadline)


# print(conf_root)
for child in conf_root:
    if child.tag == "Vertex":
        vertices[child.attrib['Name']] = Vertex(child.attrib['Name'])
    if child.tag == "Edge":
        e = Edge(child.attrib['Id'], child.attrib['BW'],
                            child.attrib['PropDelay'], child.attrib['Source'],
                            child.attrib['Destination'])
        edges.append(e)
        # print(child.attrib['Source'])
        # print(child.attrib['Destination'])
        # print(vertices)

        vertices.get(child.attrib['Source']).Egress.append(e)


        # .Egress.append(e)
        vertices.get(child.attrib['Destination']).Ingress.append(e)

for v in vertices:
    print(vertices[v])

# for e in edges:
#     print(e)

#for child in root:
##     if child.tag == "Application":
#        for g_child in child:
#            newTask = Task(Id=g_child.attrib['Id'], Period=g_child.attrib['Period'], Deadline=g_child.attrib['Deadline'], WCET=g_child.attrib['WCET'])
#            tasks.append(newTask)

#    if child.tag == "Platform":
#        for g_child in child:
#            #Ini Chips
#            newChip = Chip(g_child.attrib['Id'])
#            for g_g_child in g_child:
#                #Ini Cores
#                newCore = Core(Id=g_g_child.attrib['Id'], WCETFactor=g_g_child.attrib['WCETFactor'])
#                newChip.addCore(newCore)    #TODO remove newCore.Id from the value field
#            chips.append(newChip)
