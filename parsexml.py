import xml.etree.ElementTree as ET

tasks = []
cores = []
tree = ET.parse('small.xml')
root = tree.getroot()

for child in root:
    if child.tag == "Application":
        for g_child in child:
            tasks.append(g_child.attrib)

    if child.tag == "Platform":
        for g_child in child:
            for g_g_child in g_child:
                g_g_child.set('MCP', g_child.get('Id'))
                cores.append(g_g_child.attrib)

print(tasks)
print(cores)
