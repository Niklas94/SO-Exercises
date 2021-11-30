import xml.etree.ElementTree as ET
import math
from typing import List

CycleLength = 12

class Vertex:
    def __init__(self, Name : str):
        self.Name : str = Name
        self.Ingress : List[Edge]= []
        self.Egress : List[Edge] = []

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
        # Bandwidth is in MBit/s, but Capacity should be Bytes/c?
        # Example of bandwidth of 1000 Mbit/s
        # (1000 MBit/s) / 8 = 125 MByte/s
        # (125 MByte/s) / 10^6 = 0.000125 MByte/micro_s
        # (0.000125 MByte/micro_s) * 10^6 = 125 Byte/micro_s
        self.Capacity : int = (self.Bandwidth//8) * CycleLength
        self.InducedDelay : int = math.ceil(self.PropDelay / CycleLength)

    def __str__(self):
        return ("Id: " + self.Id + ", Bandwidth: " + str(self.Bandwidth) + ", PropDelay: " + str(self.PropDelay) + ", Source: " + self.Source + ", Destination: " + self.Destination + ", Capacity: " + str(self.Capacity) + ", Induced Delay: " + str(self.InducedDelay))

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
        if (((cycle * CycleLength) % self.Period) == 0):
            return self.Size
        else:
            return 0

    def __str__(self):
        return ("Name: " + self.Name + ", Source: " + self.Source + ", Destination: " + self.Destination + ", Size: " + str(self.Size) + ", Period: " + str(self.Period) + ", Deadline: " + str(self.Deadline) + ", Acceptable Deadline: " + str(self.AcceptableDeadline))


class Route:
    def __init__(self, Msg: Message):
        self.Msg : Message = Msg
        self.LinkAssignments : List[LinkAssignment] = []
        self.E2E : int = 0
        self.Id : str = ""

    def CalculateE2E(self):
        E2E = 0
        for la in self.LinkAssignments:
            E2E += la.Link.InducedDelay + la.QueueNumber

        self.E2E = E2E

    def MeetsDeadline(self):
        if (self.E2E > self.Msg.AcceptableDeadline):
            return False
        else :
            return True

    def __str__(self) -> str:
        ret = "------------------Route for Message------------------------\n"
        self.CalculateE2E()
        ret += self.Msg.__str__() + ", E2E: " + str(self.E2E) + ", Id: " + str(self.Id) + "\n\n"
        ret +="------------------The path---------------------\n"
        for e in self.LinkAssignments:
            ret += "\n" + e.__str__()

        ret += "\n\nMeets the acceptable deadline : " + str(self.MeetsDeadline())
        return ret


class LinkAssignment:
    def __init__(self, Link : Edge, QueueNumber : int):
        self.Link : Edge = Link
        self.QueueNumber : int = QueueNumber

    def __str__(self):
        return ("Source: " + str(self.Link.Source) + ", Destination: " + str(self.Link.Destination) + ", QueueNumber: " + str(self.QueueNumber))

class Solution:
    def __init__(self):
        self.Routes : List[Route] = []
        self.ObjectiveValue : int = 0
        self.MeanE2E : int = 0

    def __str__(self):
        ret = ("ObjectiveValue: " + str(self.ObjectiveValue) + ", MeanE2E: " +
               str(self.MeanE2E))
        for ro in self.Routes:
            ret += "\n" + ro.__str__()
        return ret


def parse(conf='./Config.xml', app='./Apps.xml') :
    vertices : dict[str, Vertex] = {}
    edges : List[Edge] = []
    msgs : List[Message] = []

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

            eg = vertices.get(child.attrib['Source'])
            if eg != None:
                eg.Egress.append(e1)

            # Add inverse edge as full duplex
            e2 = Edge(child.attrib['Id'], child.attrib['BW'],
                      child.attrib['PropDelay'], child.attrib['Destination'],
                      child.attrib['Source'])
            edges.append(e2)

            eg = vertices.get(child.attrib['Destination'])
            if eg != None:
                eg.Egress.append(e2)

    for child in app_root:
        msgs.append(Message(child.attrib['Name'], child.attrib['Source'],
                            child.attrib['Destination'], child.attrib['Size'],
                            child.attrib['Period'], child.attrib['Deadline']))
    return (vertices, edges, msgs)
