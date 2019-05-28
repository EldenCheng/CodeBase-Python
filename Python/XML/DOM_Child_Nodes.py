# -*- coding: UTF-8 -*-
from xml.dom.minidom import parse
import xml.dom.minidom

#Open the XML file, DOMTree is a Document Object
DOMTree = xml.dom.minidom.parse(r"PURORD_ECI_KERRY_StressTest.xml")


# Pls notice n is Node 3_List Object, and root is a Element object
# And the firstChild / lastChild of n is root, as root has no any other brother node
n = DOMTree.childNodes

root = DOMTree.documentElement

print(n)

print(root)

e = n[0].childNodes

e2 = e[1].childNodes

print(e2)

# Envelope, the same as above
e2 = n[0].childNodes[1].childNodes

#EnvelopeIdentification
e3 = n[0].childNodes[1].childNodes[9]

#Date
e4 = n[0].childNodes[1].childNodes[13].childNodes[1]
#Time
e5 = n[0].childNodes[1].childNodes[13].childNodes[3]

print(e2)

print(e3)

print(e4)

print(e5)


