import xml.etree.ElementTree as ET
from operator import attrgetter
import random

tasks = []
cores = []
tree = ET.parse('small.xml')
root = tree.getroot()


# Reading from xml
for child in root:
    if child.tag == "Application":
        for g_child in child:
            tasks.append(g_child.attrib)

    if child.tag == "Platform":
        for g_child in child:
            for g_g_child in g_child:
                p = g_g_child.attrib
                p['mcpID'] = g_child.attrib['Id']
                cores.append(g_g_child.attrib)

# Randomize initial solution
for item in tasks:
    coreToBeBinded = random.choice(cores)
    item['MCP'] = coreToBeBinded['mcpID']
    item['Core'] = coreToBeBinded['Id']
    print ('task: ', item)
    
