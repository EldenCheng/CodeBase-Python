'''
File 是Python的核心数据类型，这与其它绝大部分的语言都不同
File对象的实例只能由内置方法open创建
'''

# 使用建立一个open方法建立一个新的文本文件
f = open("Text.html", "w")
print("# 使用建立一个open方法建立一个新的文本文件:", f)

# 使用write方法向文本文件写入文本
f.write("Hello world\n")
print("使用write方法向文本文件写入文本:", f)

# 使用close方法关闭文件
f.close()
print("使用close方法关闭文件:", f)

# 以文件只读方式打开文件
f = open("Text.html") # 等同与 f = open("textText.txt", "r")
text = f.read()
print("以只读方式打开文件:", text)

# 以二进制只读方式打开文件
f = open("wesoft.png", "rb")
b = f.read()
print("以二进制只读方式打开文件:", b[0:10])