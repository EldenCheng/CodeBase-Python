from lxml import etree
"""
API文档可以参考 https://lxml.de/api/lxml.etree._ElementTree-class.html
"""

if __name__ == '__main__':
    # 基本打开xml文件的方法
    tree = etree.parse("uidump.xml")

    # 获取xml文档的一些信息
    # 也可以获取这个tree的parser
    docinfo = tree.docinfo
    parser = tree.parser

    # 获取根节点
    root = tree.getroot()

    # 可以使用for循环来遍历所有子节点
    for node in root:
        print(node.attrib["bounds"])

    # 通过xpath查找元素
    xpath_result = tree.xpath('//*[@text="在设置中搜索"]')[0]
    # xpath_result = tree.xpath('//*[@text="网络和互联网"]')[0]

    # 获取元素路径
    element_path = tree.getelementpath(xpath_result)
    # 获取绝对路径(即从root开始)
    ab_path = tree.getpath(xpath_result)
    print(element_path)
    print(ab_path)

    # 通过路径查找元素, 会默认返回第一个符合要求的元素
    path_result = tree.find("node/node[2]/node[3]/node[1]")
    # 可以使用get('text')方法来获取属性值, 也可以使用attrib['text']属性来获取属性值
    # 使用get方法的好处是拿不到对应的属性值不会报错
    print(path_result.get("text"))

    # 可以使用findall来查找所有符合要求的元素
    path_results = tree.findall("node/node[2]/node[3]/node")
    for pr in path_results:
        print(pr.attrib['text'])

    # 如果有新的xml文件需要解释, 可以直接使用parse方法来更新tree的内容
    tree.parse("PURORD_ECI_KERRY_StressTest.xml")
    new_root = tree.getroot()
    print(new_root.tag)

    # 将tree内容写入文件
    file = open("temp_test.xml", "w")
    file.close()
    tree.write("temp_test.xml", encoding='utf-8')




