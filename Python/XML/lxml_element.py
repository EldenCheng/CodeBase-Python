from lxml import etree, objectify
import re
"""
API文档可以参考 https://lxml.de/api/lxml.etree._Element-class.html
"""

if __name__ == '__main__':
    # 基本打开xml文件的方法
    tree = etree.parse("uidump.xml")

    node = tree.find("node/node[2]/node[3]")

    # 直接获得所有子元素
    sub_nodes = node.getchildren()

    for sn in sub_nodes:
        print(sn.get('text'))

    # 通过指定路径获得子元素
    sub_node = node.find("node[2]")
    print(sub_node.get('text'))

    # 也可以使用xpath查找元素, 注意不限于子元素
    sub_node = node.xpath('//*[contains(@text,"搜索")]')[0]
    print(sub_node.get('text'))

    # 通过指定前后位置获得兄弟元素
    node2 = tree.find("node/node[2]/node[3]/node")
    next_node = node2.getnext()
    print(next_node.get('text'))
    previous_node = next_node.getprevious()
    print(previous_node.get('text'))

    # 在当前tree中插入元素
    # objectify包的API请参考
    # https://lxml.de/api/toc-lxml.objectify-module.html
    new_element = objectify.Element("test")

    next_node.addnext(new_element)
    sub_nodes = node.getchildren()

    for sn in sub_nodes:
        print(sn.tag)

    bounds = "[0,0][1080,2034]"
    coord = re.compile(r"\d+").findall(bounds)
    print(coord)

