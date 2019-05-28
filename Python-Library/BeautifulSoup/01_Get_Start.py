"""
BeautifulSoup是Python的一个库，最主要的功能就是从网页爬取我们需要的数据。BeautifulSoup将html解析为对象进行处理，
全部页面转变为字典或者数组，相对于正则表达式的方式，可以大大简化处理过程。

不过要注意现代的很多网站采取动态读取技术, 很多时候request.get获取到的最初的html并没有包含完全的网页所有的内容, 可能要先想办法加载了才可以
"""

"""
BeautifulSoup默认支持Python的标准HTML解析库，但是它也支持一些第三方的解析库：

序号	  解析库	                     使用方法	                        优势	                    劣势
1	Python标准库	    BeautifulSoup(html,’html.parser’)	Python内置标准库;执行速度快	    容错能力较差
2	lxml HTML解析库	BeautifulSoup(html,’lxml’)	        速度快；容错能力强	            需要安装，需要C语言库
3	lxml XML解析库	BeautifulSoup(html,[‘lxml’,’xml’])	速度快；容错能力强；支持XML格式	需要C语言库
4	htm5lib解析库	    BeautifulSoup(html,’htm5llib’)	    以浏览器方式解析，最好的容错性	速度慢
--------------------- 
"""

if __name__ == '__main__':

    # 导入对象

    from bs4 import BeautifulSoup
    import requests

    # 创建HTML实例

    html = requests.get("https://www.wine.com/")

    # 创建 Beautiful Soup 对象
    bs = BeautifulSoup(html.text, 'html5lib')

    f = open("Text.html", "w")
    f.write(html.text)
    f.close()

    # 支持提出HTML标签的内容, 主要是name, text, attrs, children, contents, hidden, is_empty_element等等, 可以用debug查看标签对象
    print(bs.h1.name)
    print(bs.h1.text)
    print(bs.h1.attrs)
    print(bs.h1.children)
    print(bs.h1.contents)
    print(bs.h1.hidden)
    print(bs.h1.is_empty_element)







