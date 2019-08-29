"""
下面演示的是find方法下查找父,子,兄弟节点, 同样find_all方法也有相对应的方法
"""
from bs4 import BeautifulSoup
import requests

if __name__ == '__main__':
    html = requests.get("https://www.wesoft.com/")
    bs = BeautifulSoup(html.text, 'html5lib')

    tab = bs.find(class_='fusion-standard-logo')  # 找到当前元素
    print(tab['class'])
    parent = tab.find_parent()  # 当前元素的父元素
    print(parent['class'])
    brothers = parent.findChildren()  # 父元素的子元素们
    for b in brothers:
        print(b['class'])

    next_tab = tab.find_next()  # 当前元素的下一个元素, 注意如果找不到不会报错而是会返回None
    if next_tab:
        print(next_tab['class'])

    prev_tab = tab.find_previous()  # 当前元素的上一个元素, 注意如果找不到不会报错而是会返回None
    if prev_tab:
        print(prev_tab['class'])



