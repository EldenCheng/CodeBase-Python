from xml.dom.minidom import parse
import xml.dom.minidom

tree = xml.dom.minidom.parse(r"PURORD_ECI_KERRY_StressTest.xml")
root = tree.documentElement

POM = root.getElementsByTagName("PurchaseOrderMessage")[0]

# 在添加子节点时，一定要用cloneNode，不然的话会变成将指定的节点移动到最后而不是添加一个
root.appendChild(root.childNodes[0].cloneNode(True))
root.appendChild(POM.cloneNode(True))
# 如果要循环使用，需要将指针指向最新的节点
POM = root.getElementsByTagName("PurchaseOrderMessage")[1]