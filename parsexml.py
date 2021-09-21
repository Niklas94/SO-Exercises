import xml.etree.ElementTree as ET
from operator import attrgetter
import random

tasks = []
cores = []
c_t = {}
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
    if (coreToBeBinded['mcpID'], coreToBeBinded['Id']) in c_t:
        c_t[(coreToBeBinded['mcpID'], coreToBeBinded['Id'])].append(item['Id'])
    else:
        c_t[(coreToBeBinded['mcpID'], coreToBeBinded['Id'])] = [item['Id']]
    # print ('task: ', item)

print(c_t)

# print(cores)
