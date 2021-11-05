from lxml import etree

if __name__ == '__main__':
    # 基本打开xml文件的方法
    tree = etree.parse("uidump.xml")

    # XML方法只能解释string里的xml语句, 不能打开文件里的xml语句, 并且不支持utf-8字符
    try:
        xml = etree.XML('<?xml version="1.0" encoding="UTF-8"?>')
    except Exception as msg:
        print(msg)

    result = tree.xpath('//*[@text="在设置中搜索"]')[0]  # 使用节点属性查找
    print(result.tag)  # 获取节点名称
    print(result.attrib["bounds"])  # 获取节点属性
    results = tree.xpath('//*[contains(@text, "搜索")]')  # 使用节点属性模糊搜索查找
    for r in results:
        print(r.attrib["bounds"])

    # child = tree.xpath('//*[@text="在设置中搜索"]')
