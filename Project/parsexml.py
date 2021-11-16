import xml.etree.ElementTree as ET
from operator import attrgetter
import random
import math
from xml.dom import minidom

CycleLength = 12

class Vertex:
    def __init__(self, Name : str):
        self.Name : str = Name
        self.Ingress : list[Edge]= []
        self.Egress : list[Edge] = []

    def __str__(self) -> str:
        ret =  "Name: " + self.Name + "\nIngress: "
        for i in self.Ingress:
            ret += "\n" + i.__str__() + ", "
        ret += "\nEgress: "
        for e in self.Egress:
            ret += "\n" + e.__str__() + ", "
        return ret + "\n\n"

class Edge:
    def __init__(self, Id : str, Bandwidth : str, PropDelay : str, Source : str,
                 Destination : str):
        self.Id : str = Id
        self.Bandwidth : int = int(Bandwidth)
        self.PropDelay : int = int(PropDelay)
        self.Source : str = Source
        self.Destination : str = Destination
        self.Capacity : int = self.Bandwidth * CycleLength
        self.InducedDelay : int = math.floor(self.PropDelay / CycleLength)

    def __str__(self) -> str:
        return ("Id: " + self.Id + ", Bandwidth: " + str(self.Bandwidth) + ", PropDelay: " + str(self.PropDelay) + ", Source: " + self.Source + ", Destination: " + self.Destination)

    def __eq__(self, other) -> bool:
        if isinstance(other, Edge):
            return self.Id == other.Id
        else:
            return False

class Message:
    def __init__(self, Name : str, Source : str, Destination : str, Size : str,
                 Period : str, Deadline: str):
        self.Name : str = Name
        self.Source : str = Source
        self.Destination : str = Destination
        self.Size : int = int(Size)
        self.Period : int = int(Period)
        self.Deadline : int = int(Deadline)
        self.AcceptableDeadline : int = math.floor(int(Deadline) / CycleLength)

    def ArrivalPattern(self, cycle : int) -> int:
        if (not ((cycle * CycleLength) % self.Period)):
            return self.Size
        else:
            return 0

    def __str__(self) -> str:
        return ("Name: " + self.Name + ", Source: " + self.Source + ", Destination: " + self.Destination + ", Size: " + str(self.Size) + ", Period: " + str(self.Period) + ", Deadline: " + str(self.Deadline))

class Route:
    def __init__(self, Msg: Message):
        self.Msg : Message = Msg
        self.LinkAssignments : list[LinkAssignment] = []
        self.E2E : int = 0

    def __str__(self) -> str:
        ret = self.Msg.__str__() + ", E2E: " + str(self.E2E)
        for e in self.LinkAssignments:
            ret += "\n" + e.__str__()
        return ret


class LinkAssignment:
    def __init__(self, Link : Edge, QueueNumber : int):
        self.Link : Edge = Link
        self.QueueNumber : int = QueueNumber

    def __str__(self):
        return ("Link: " + self.Link.__str__() + "QueueNumber: " + str(self.QueueNumber))


def parse(conf='ConfigTest.xml', app='Appstest.xml') -> tuple[dict[str,Vertex],
                                                              list[Edge],
                                                              list[Message]]:
    vertices : dict[str, Vertex] = {}
    edges : list[Edge] = []
    msgs : list[Message] = []

    conf_tree : ET.ElementTree = ET.parse(conf)
    conf_root : ET.Element = conf_tree.getroot()
    app_tree : ET.ElementTree = ET.parse(app)
    app_root : ET.Element = app_tree.getroot()

    for child in conf_root:
        if child.tag == "Vertex":
            vertices[child.attrib['Name']] = Vertex(child.attrib['Name'])
        if child.tag == "Edge":
            # Add original edge
            e1 = Edge(child.attrib['Id'], child.attrib['BW'],
                                child.attrib['PropDelay'], child.attrib['Source'],
                                child.attrib['Destination'])
            edges.append(e1)

            vertices.get(child.attrib['Source']).Egress.append(e1)
            vertices.get(child.attrib['Destination']).Ingress.append(e1)

            # Add inverse edge as full duplex
            e2 = Edge(child.attrib['Id'], child.attrib['BW'],
                      child.attrib['PropDelay'], child.attrib['Destination'],
                      child.attrib['Source'])
            edges.append(e2)

            vertices.get(child.attrib['Destination']).Egress.append(e2)
            vertices.get(child.attrib['Source']).Ingress.append(e2)

    for child in app_root:
        msgs.append(Message(child.attrib['Name'], child.attrib['Source'],
                            child.attrib['Destination'], child.attrib['Size'],
                            child.attrib['Period'], child.attrib['Deadline']))
    return (vertices, edges, msgs)
