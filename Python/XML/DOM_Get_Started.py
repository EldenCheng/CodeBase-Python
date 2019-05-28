# -*- coding: UTF-8 -*-
from xml.dom.minidom import parse
import xml.dom.minidom

#Open the XML file, DOMTree is a Document Object
DOMTree = xml.dom.minidom.parse("PURORD_ECI_KERRY_StressTest_002.xml")


# Get the xml root node
n = DOMTree.documentElement

# Print the info of the root node
print(n.nodeName)
print(n.nodeValue)
print(n.nodeType)
print(n.ELEMENT_NODE)

#Node type code: 1 = Element node 3 = Text node 8 = Comment node

# Get the sub node of root

sub = n.getElementsByTagName('Identification')

for s in sub:
    print(s.nodeName)
    print(s.nodeValue)
    print(s.nodeType)
    print(s.ELEMENT_NODE)
    print(s.firstChild.data)
    print(s.firstChild.nodeValue)





