'''
Python属性__name__有两种用法, 第一种是如果本段代码是程序入口, __name__的值为"__main__"
如果是普通代码, 则为包名+模块名
'''

#如果直接运行这段代码, 这里将打印出"__main__"
print(__name__)

print("when import")

