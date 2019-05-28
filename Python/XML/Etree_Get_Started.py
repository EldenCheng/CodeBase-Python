from xml.etree import ElementTree

#Open the xml file
tree = ElementTree.parse(r'.\Ori\PURORD_ECI_KERRY_StressTest.xml')

#Get the root node
root = tree.getroot()

#print(root)

# Print the tag name and attrib of all the child nodes of root
#for child in root:
#    print(child.tag, child.attrib)

#Get the first child node of root
envelope = root[0]

#print(envelope)

# Print the tag name and attrib of all the child nodes of envelope
#for child in envelope:
#    print(child.tag, child.attrib)

#Find a node with a path, if multi nodes, use findall
date = envelope.find("TransmissionDateTime/Date")

#Print the value of this node
print(date.text)

#Modify the value of node
date.text = "2017-09-06"

print(date.text)

#Save the xml file

tree.write("Result.xml", encoding="utf-8",xml_declaration=True)
