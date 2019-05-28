from xml.etree import ElementTree

#Open the xml file
tree = ElementTree.parse(r'.\Ori\PURORD_ECI_KERRY_StressTest.xml')

#Get the root node
root = tree.getroot()

POM = root[1]

root.append(POM)

for child in root:
    print(child.tag)

#Save the xml file
tree.write(".\Des\Result1.xml", encoding="utf-8",xml_declaration=True)
