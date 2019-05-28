"""
一般来说上面以标签访问的都是第一个符合条件的标签, 如果我们想查找多个或者某一个符合条件但不是排第一的标签时,可以使用查找方法
1. find all方法: 具体的方法参考是find_all( name , attrs , recursive , text , **kwargs )
                其中name是指标签的名字,比如title, a, div, span等等
"""

if __name__ == '__main__':

    # 导入对象

    from bs4 import BeautifulSoup
    import requests
    import re

    html = requests.get("https://www.wine.com/")
    bs = BeautifulSoup(html.text, 'html5lib')

    # find all 方法
    # name参数
    # 支持直接写标签名字
    tabs = bs.find_all('span')
    for t in tabs:
        print(t.text)

    # 支持使用列表
    tabs = bs.find_all(('title', 'h1'))
    for t in tabs:
        print(t.text)

    # 支持使用正则表达式
    tabs = bs.find_all(re.compile('^b'))  # 所有以b开头的标签对象都会被找到
    for t in tabs:
        print(t.text)

    # 使用attrs参数
    # 实际上可以支持直接写id=xx, href=xx这样的,也支持以字典形式传入
    # 不过由于class是Python关键字, 所以要写成class_=xx
    # 后面的这个=xx的xx是同样支持直接输入关键字字符串,列表,正则表达式的
    tabs = bs.find_all(class_='mainNavList_item mainNavList_item-level3')
    for t in tabs:
        print(t.text)

    # 当然也支持同时指定多个条件
    tabs = bs.find_all(name='a', class_='mainNavList_itemLink', href='/list/wine/red-wine/7155-124')
    print("同时指定多个条件")
    for t in tabs:
        print(t.text)

    # 要注意使用text参数是用来搜索HTML中的字符串内容的而不是用来查找标签的
    # 同样支持直接输入关键字字符串,列表,正则表达式
    # 一般来说获得的结果是一个列表, 列表的元素就是在HTML中出现过符合关键字的text
    texts = bs.find_all(text='Red Wine')
    print("使用text参数")
    print("在HTML中符合关键字的文本数量为: ", len(texts))
    for t in texts:
        print(t)

    # recursive参数
    # recursive参数的作用是限制BS搜索的深度, 当指定recursive为False时搜索深度仅仅为当前节点的下一级节点,
    # 为True为搜索下级所有节点(这个是默认值)

    texts1 = bs.find_all(text='Red Wine', recursive=False)
    print("使用recursive参数")
    print("当recursive参数为False时Red Wine的个数: ", len(texts1))
    for t in texts1:
        print(t)



