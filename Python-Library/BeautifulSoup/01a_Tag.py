"""
Tag 是XML或者HTML原生文档中的元素标签对象, 实际上BS实例化是就是生成了对应HTML或者XML的Tag的集合
"""

# 导入对象

from bs4 import BeautifulSoup
import requests

if __name__ == '__main__':
    # 创建HTML实例
    html = requests.get("https://www.wine.com/")

    # 创建 Beautiful Soup 对象
    bs = BeautifulSoup(html.text, 'html5lib')
    tag_h1 = bs.h1
    print(type(tag_h1))
    print("tag's name: ", tag_h1.name)  # 实际上与bs.h1.name是一样的, 注意name是tag本身的名字,比如h1的名字就是h1, tag的内容要用text来获取
    print("tag's all attributes: ", tag_h1.attrs)  # 是一个字典的集合
    print("tag's class attribute: ", tag_h1['class'])
