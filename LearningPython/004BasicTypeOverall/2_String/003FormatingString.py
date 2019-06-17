"""
Python中格式化字符串可以使用占位符与字符串格式化方法
"""
s1 = "Hello, my %s, I love %s!" % ("friend", "you")

print("使用占位符:", s1)

s2 = "Hello, my {0}, I love {1}".format("friend", "you")
print("使用字符串方法:", s2)

s4 = "Hello, my {0}, I love {0}".format("friend", "you")
print("使用字符串方法:", s4)

# 方法的参数不能直接放元组或者列表， 只能如下面这样用
s3 = ("friend", "you")
s2 = "Hello, my {0}, I love {1}".format(s3[0], s3[1])
print("使用字符串方法:", s2)
