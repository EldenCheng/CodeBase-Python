# -*- coding: UTF-8 -*-
from xml.dom.minidom import parse
import xml.dom.minidom

#Open the XML file
DOMTree = xml.dom.minidom.parse("PURORD_ECI_KERRY_StressTest_002.xml")


# Get the xml root node
n = DOMTree.documentElement

sub = n.getElementsByTagName('Identification')

s = sub[0]

#Update the nodeValue
s.firstChild.nodeValue = "XMLTest"

print(s.firstChild.nodeValue)

#Create a blank file
f = open("XMLResult.xml", "w")

#Save the xml content to the file
DOMTree.writexml(f)
