import xml.etree.ElementTree as ET
from operator import attrgetter
import random
from xml.dom import minidom


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
            ret += "\n" + e.__str__() + ", "
        return ret + "\n\n"

class Edge:
    def __init__(self, Id, Bandwidth, PropDelay, Source, Destination):
        self.Id = Id
        self.Bandwidth = Bandwidth
        self.PropDelay = PropDelay
        self.Source = Source
        self.Destination = Destination

    def __str__(self):
        return ("Id: " + self.Id + ", Bandwidth: " + self.Bandwidth + ", PropDelay: " + self.PropDelay + ", Source: " + self.Source + ", Destination: " + self.Destination)

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
        return ("Name: " + self.Name + ", Source: " + self.Source + ", Destination: " + self.Destination + ", Size: " + self.Size + ", Period: " + self.Period + ", Deadline: " + self.Deadline)

class Msg2Route:
    def __init__(self, Msg):
        self.Msg = Msg
        self.Route = []
        self.E2E = 0

    def __str__(self):
        ret = self.Msg.__str__() + ", E2E: " + str(self.E2E)
        for e in self.Route:
            ret += "\n" + e.__str__()
        return ret

def parse(conf='ConfigTest.xml', app='Appstest.xml'):
    vertices = {}
    edges = []
    msgs = []

    conf_tree = ET.parse(conf)
    conf_root = conf_tree.getroot()
    app_tree = ET.parse(app)
    app_root = app_tree.getroot()

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
