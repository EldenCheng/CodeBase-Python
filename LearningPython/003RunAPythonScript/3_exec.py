"""
exec方法可以在当前script中动态引入python或者python模块
当它引入python模块里, 实际上像from... import ...一样是将模块的代码复制到当前位置
所以一样要注意属性名, 类名之类的被当前script中同名属性或者类覆盖的问题
更多的关于exec方法的内容在第9章
"""

if __name__ == "__main__":
    exec("print('hello world')")
    exec(open('2_reload.py', "r", encoding='utf-8').read())  # 可以把整个py文件打开来运行
