'''
字串符除了是序列之外，还是一种特立的数据类型，所以可以使用序列的方法之外，实际上也有它自己特有的方法
'''

s1 = "a string test"
s2 = "Hello, my friend,I love you!"

# 查找子串位置
index = s1.find("test")
print("子串位置", index)

# 替换子串
s1 = s1.replace("test", "replacement")
print("子串替换", s1)

# 大小写转换
s1 = s1.upper()
print("大写:", s1)

s1 = s1.lower()
print("小写:", s1)

s1 = s1.swapcase()
print("转换大小写:", s1)
s1 = s1.swapcase()
print("转换大小写:", s1)

s1 = s1.capitalize()
print("首字母大写", s1)

# 拆分字符串
s2 = s2.split(",") # 会返回一个字符串数组
print("拆分字符串", s2)