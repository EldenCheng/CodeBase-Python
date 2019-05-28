from xml.dom.minidom import parse
import xml.dom.minidom

tree = xml.dom.minidom.parse(r"PURORD_ECI_KERRY_StressTest.xml")
root = tree.documentElement

# 要注意通过getElementsByTagName或者root.childNodes[0]这样的下标来获得的，都是元素集合(节点)，
# 就算实际上获取的结果只有一个元素，那也是有一个元素的集合
# 所以获取到元素集合后，一定要通过属性.firstChild来访问，例如最下面的.firstChild.nodeValue
# 另外的下标[0]代表找到的第一个元素集合(节点)

POM = root.getElementsByTagName("PurchaseOrderMessage")[0]

# 这个实际上就是路径 PurchaseOrderNumber/Reference
POM.getElementsByTagName("PurchaseOrderNumber")[0].getElementsByTagName("Reference")[0].firstChild.nodeValue = 1