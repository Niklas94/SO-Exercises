# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 18:15:27 2021

@author: SölviPálsson
"""

import xml.etree.cElementTree as ET
from xml.dom import minidom
from parsexml import Route, LinkAssignment, Solution


def solutionToXml(runtime, solution: Solution):
    root = ET.Element("Report")

    tree = ET.SubElement(root, "Solution")


    tree.set("MeanBW", str(solution.ObjectiveValue))
    tree.set("MeanE2E", str(solution.MeanE2E))
    tree.set("Runtime", str(runtime))


    r : Route
    linkAssignment : LinkAssignment

    for r in solution.Routes:
        msg = ET.SubElement(root, "Message")
        msg.set("Name", r.Msg.Name)
        msg.set("MaxE2E", str(r.E2E))

        for linkAssignment in r.LinkAssignments:

            link = ET.SubElement(msg, "Link")
            link.set("Source", linkAssignment.Link.Source)
            link.set("Destination", linkAssignment.Link.Destination)
            link.set("Qnumber", str(linkAssignment.QueueNumber))


    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
    with open("Report.xml", "w") as f:
        f.write(xmlstr)


