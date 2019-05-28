"""
BS中也支持使用CSS selector来查找标签
"""

if __name__ == '__main__':

    # 导入对象

    from bs4 import BeautifulSoup
    import requests

    html = requests.get("https://www.wine.com/")
    bs = BeautifulSoup(html.text, 'lxml')

    # 标签选择器
    h1 = bs.select('h1')
    # print(h1.text)
    for h in h1:
        print(h.text)
    # 类名选择器
    spans_with_class = bs.select('span.scrollerList_title')  # 内容需要JS动态加载, 所以普通状态下找不到

    p_with_class = bs.select('p.tooltipComponent_text')
    for p in p_with_class:
        print(p.text)
    # id选择器
    bs.select('#css')
    # 属性选择器
    bs.select('a[class="css"]')
